import asyncio
import json
import re

from loguru import logger

from ...l1.schema import Opinion, IdeaPool, DivergentPoint, UniquePoint
from ...l2.panelist import Panelist

_PANEL_SYSTEM_MSG = (
    "You are an expert providing your independent analysis. "
    "Be specific, thorough, and present your unique perspective."
)

_SUMMARIZER_SYSTEM_MSG = (
    "You are an analyst. Given multiple expert opinions on an agenda, "
    "classify the key points into three categories.\n"
    "Respond ONLY in valid JSON with this exact structure:\n"
    "{\n"
    '  "common": ["point shared by most experts", ...],\n'
    '  "divergent": [{"topic": "topic", "positions": {"Expert1": "position", "Expert2": "position"}}, ...],\n'
    '  "unique": [{"point": "insight", "source_model": "ExpertName"}, ...]\n'
    "}\n"
    "Rules:\n"
    "- common: points that 2+ experts agree on\n"
    "- divergent: topics where experts have clearly different positions\n"
    "- unique: points raised by only one expert\n"
    "- Be thorough, do not lose information\n"
    "- Respond in the same language as the opinions"
)


class Roundtable:
    def __init__(self, panelists: list[Panelist], summarizer: Panelist):
        self.panelists = panelists
        self.summarizer = summarizer
        logger.info(f"Roundtable 구성: 패널 {len(panelists)}명")

    async def gather(self, agenda: str, context: str = "") -> list[Opinion]:
        prompt = self._build_prompt(agenda, context)
        tasks = [p.ask_async(prompt, _PANEL_SYSTEM_MSG) for p in self.panelists]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        opinions = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                name = self.panelists[i].model_entry.display_name
                logger.warning(f"패널 {name} 실패, 제외: {result}")
                continue
            opinions.append(result)

        logger.info(f"의견 수집: {len(opinions)}/{len(self.panelists)}")
        return opinions

    async def summarize(self, agenda: str, opinions: list[Opinion]) -> IdeaPool:
        opinions_text = "\n\n".join(
            f"--- {op.model_name} ---\n{op.content}" for op in opinions
        )
        prompt = f"Agenda: {agenda}\n\nExpert Opinions:\n{opinions_text}"

        result = await self.summarizer.ask_async(prompt, _SUMMARIZER_SYSTEM_MSG)
        parsed = self._extract_json(result.content)

        # 비용 합산: 패널 + summarizer
        total_cost = sum(op.cost for op in opinions) + result.cost
        total_tokens = sum(op.tokens for op in opinions) + result.tokens

        return IdeaPool(
            agenda=agenda,
            common=parsed.get("common", []),
            divergent=[DivergentPoint(**d) for d in parsed.get("divergent", [])],
            unique=[UniquePoint(**u) for u in parsed.get("unique", [])],
            total_cost=total_cost,
            total_tokens=total_tokens,
        )

    async def discuss(self, agenda: str, context: str = "") -> tuple[IdeaPool, list[Opinion]]:
        opinions = await self.gather(agenda, context)
        if not opinions:
            logger.warning("수집된 의견 없음")
            pool = IdeaPool(agenda=agenda, common=[], divergent=[], unique=[])
            return pool, []
        pool = await self.summarize(agenda, opinions)
        return pool, opinions

    def _build_prompt(self, agenda: str, context: str = "") -> str:
        parts = [f"Agenda: {agenda}"]
        if context:
            parts.insert(0, f"Context: {context}")
        return "\n\n".join(parts)

    def _extract_json(self, text: str) -> dict:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if match:
            text = match.group(1)

        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError(f"JSON 파싱 실패: {text[:200]}")

        return json.loads(text[start:end + 1])
