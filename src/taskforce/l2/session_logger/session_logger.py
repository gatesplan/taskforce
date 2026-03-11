import json
from datetime import datetime
from pathlib import Path

from loguru import logger

from ...l1.schema import Opinion

_DEFAULT_DIR = Path.home() / ".taskforce" / "logs"


class SessionLogger:
    def __init__(self, log_dir: Path | None = None):
        self.log_dir = log_dir or _DEFAULT_DIR
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log(self, agenda: str, context: str, opinions: list[Opinion], summarizer_output: str = "") -> Path:
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        filepath = self.log_dir / f"{timestamp}.jsonl"

        with open(filepath, "a", encoding="utf-8") as f:
            # 의제 기록
            f.write(json.dumps({
                "type": "request",
                "timestamp": timestamp,
                "agenda": agenda,
                "context": context,
            }, ensure_ascii=False) + "\n")

            # 각 패널 응답 기록
            for op in opinions:
                f.write(json.dumps({
                    "type": "opinion",
                    "model_name": op.model_name,
                    "content": op.content,
                    "tokens": op.tokens,
                    "cost": op.cost,
                }, ensure_ascii=False) + "\n")

            # summarizer 출력 기록
            if summarizer_output:
                f.write(json.dumps({
                    "type": "summarizer",
                    "content": summarizer_output,
                }, ensure_ascii=False) + "\n")

        logger.debug(f"세션 로그 기록: {filepath}")
        return filepath
