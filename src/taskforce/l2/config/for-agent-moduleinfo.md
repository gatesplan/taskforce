# Config

.env에서 API 키를 로드하고 모델 레지스트리를 구성.

## EnvConfig

환경변수 기반 모델 구성. caller_provider 모델은 패널에서 제외.

### Properties
caller_provider: str                 # 호출자 프로바이더
panel_models: list[ModelEntry]       # 활성 패널 모델 목록
summarizer_model: ModelEntry         # Summarizer 모델 (grok-4-1-fast-non-reasoning)

### __init__
__init__(caller_provider: str, dotenv_path: str | None = None)
    raise ValueError
    .env 로드 후 키가 있고 caller가 아닌 모델만 패널 등록.
    활성 패널 0개이면 ValueError.
    XAI_API_KEY 없으면 ValueError (summarizer 필수).

### Methods

get_active_panels() -> list[ModelEntry]
    등록된 패널 모델 목록 반환.
