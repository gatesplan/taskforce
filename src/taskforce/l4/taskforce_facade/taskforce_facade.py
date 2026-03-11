import asyncio

from loguru import logger

from ...l1.schema import IdeaPool
from ...l2.config import EnvConfig
from ...l2.panelist import Panelist
from ...l2.session_logger import SessionLogger
from ...l2.cost_logger import CostLogger
from ...l3.roundtable import Roundtable


class Taskforce:
    def __init__(self, caller_provider: str, dotenv_path: str | None = None):
        self.config = EnvConfig(caller_provider, dotenv_path)

        panelists = [Panelist(m) for m in self.config.get_active_panels()]
        summarizer = Panelist(self.config.summarizer_model)
        self.roundtable = Roundtable(panelists, summarizer)

        self.session_logger = SessionLogger()
        self.cost_logger = CostLogger()

        logger.info("Taskforce 초기화 완료")

    async def discuss_async(self, agenda: str, context: str = "") -> IdeaPool:
        pool, opinions = await self.roundtable.discuss(agenda, context)

        # 로그 기록
        if opinions:
            summarizer_cost = pool.total_cost - sum(op.cost for op in opinions)
            summarizer_tokens = pool.total_tokens - sum(op.tokens for op in opinions)

            self.session_logger.log(agenda, context, opinions)
            self.cost_logger.log(agenda, opinions, summarizer_cost, summarizer_tokens)

        return pool

    def discuss(self, agenda: str, context: str = "") -> IdeaPool:
        return asyncio.run(self.discuss_async(agenda, context))
