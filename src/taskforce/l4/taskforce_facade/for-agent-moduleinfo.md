# Taskforce Facade

최상위 진입점. 초기화와 discuss 호출을 단순화.

## Taskforce

EnvConfig + Roundtable 조합을 단일 인터페이스로 노출.

### Properties
config: EnvConfig          # 환경 설정
roundtable: Roundtable     # 라운드테이블 인스턴스

### __init__
__init__(caller_provider: str, dotenv_path: str | None = None)
    raise ValueError
    EnvConfig 로드, Panelist/Roundtable 자동 구성.
    EnvConfig 실패 시 ValueError 전파.

### Methods

discuss_async(agenda: str, context: str = "") -> IdeaPool
    async 버전. roundtable.discuss 위임.

discuss(agenda: str, context: str = "") -> IdeaPool
    sync 버전. asyncio.run으로 discuss_async 실행.
