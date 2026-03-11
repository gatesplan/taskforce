import json
from datetime import datetime
from pathlib import Path

from loguru import logger

from ...l1.schema import Opinion

_DEFAULT_DIR = Path.home() / ".taskforce" / "cost_logs"


class CostLogger:
    def __init__(self, log_dir: Path | None = None):
        self.log_dir = log_dir or _DEFAULT_DIR
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log(self, agenda: str, opinions: list[Opinion], summarizer_cost: float = 0.0, summarizer_tokens: int = 0) -> None:
        timestamp = datetime.now().isoformat()

        models = []
        for op in opinions:
            models.append({
                "model_name": op.model_name,
                "tokens": op.tokens,
                "cost": op.cost,
            })

        total_cost = sum(op.cost for op in opinions) + summarizer_cost
        total_tokens = sum(op.tokens for op in opinions) + summarizer_tokens

        record = {
            "timestamp": timestamp,
            "agenda": agenda[:100],
            "models": models,
            "summarizer_cost": summarizer_cost,
            "summarizer_tokens": summarizer_tokens,
            "total_cost": total_cost,
            "total_tokens": total_tokens,
        }

        # 월별 파일로 분리
        month = datetime.now().strftime("%Y-%m")
        filepath = self.log_dir / f"{month}.jsonl"

        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        logger.debug(f"비용 로그 기록: ${total_cost:.4f}, {total_tokens} tokens")
