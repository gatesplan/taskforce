import os

from dotenv import load_dotenv
from loguru import logger

from ...l1.schema import ModelEntry

# 환경변수 -> 패널 모델 매핑
_PANEL_REGISTRY = [
    {"env_key": "OPENAI_API_KEY", "provider": "openai", "model_id": "gpt-5.4", "display_name": "GPT 5.4"},
    {"env_key": "XAI_API_KEY", "provider": "xai", "model_id": "grok-4-1-fast-reasoning", "display_name": "Grok 4-1"},
    {"env_key": "ANTHROPIC_API_KEY", "provider": "anthropic", "model_id": "claude-opus-4", "display_name": "Claude opus-4"},
    {"env_key": "GEMINI_API_KEY", "provider": "gemini", "model_id": "gemini-2.5-pro", "display_name": "Gemini 2.5 Pro"},
]

_SUMMARIZER_MODEL_ID = "grok-4-1-fast-non-reasoning"
_SUMMARIZER_DISPLAY_NAME = "Grok 4-1 Fast"


class EnvConfig:
    def __init__(self, caller_provider: str, dotenv_path: str | None = None):
        self.caller_provider = caller_provider

        if dotenv_path:
            load_dotenv(dotenv_path)
        else:
            load_dotenv()

        # caller_provider 제외, 키가 있는 모델만 패널 등록
        self.panel_models: list[ModelEntry] = []
        for entry in _PANEL_REGISTRY:
            api_key = os.getenv(entry["env_key"], "")
            if not api_key:
                continue
            if entry["provider"] == caller_provider:
                logger.debug(f"패널 제외 (caller): {entry['display_name']}")
                continue
            self.panel_models.append(ModelEntry(
                provider=entry["provider"],
                model_id=entry["model_id"],
                api_key=api_key,
                display_name=entry["display_name"],
                extra_params=entry.get("extra_params", {}),
            ))
            logger.debug(f"패널 등록: {entry['display_name']}")

        if not self.panel_models:
            raise ValueError("활성 패널 모델이 없습니다. .env에 API 키를 설정하세요.")

        # Summarizer (XAI_API_KEY 공유)
        xai_key = os.getenv("XAI_API_KEY", "")
        if not xai_key:
            raise ValueError("XAI_API_KEY 필요 (summarizer용)")

        self.summarizer_model = ModelEntry(
            provider="xai",
            model_id=_SUMMARIZER_MODEL_ID,
            api_key=xai_key,
            display_name=_SUMMARIZER_DISPLAY_NAME,
        )

        logger.info(f"EnvConfig 초기화: 패널 {len(self.panel_models)}개, caller={caller_provider}")

    def get_active_panels(self) -> list[ModelEntry]:
        return self.panel_models
