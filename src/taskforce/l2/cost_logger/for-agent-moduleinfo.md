# CostLogger

비용 요약 로그 기록. 모델별 tokens/cost를 JSONL로 저장.

## CostLogger

~/.taskforce/cost_logs/ 에 월별 JSONL 파일로 누적 기록.

### Properties
log_dir: Path              # 로그 디렉토리 경로

### __init__
__init__(log_dir: Path | None = None)
    log_dir 미지정 시 ~/.taskforce/cost_logs/ 사용.
    디렉토리 자동 생성.

### Methods

log(agenda: str, opinions: list[Opinion], summarizer_cost: float = 0.0, summarizer_tokens: int = 0) -> None
    비용 레코드를 월별 파일에 append.
    모델별 tokens/cost + 총계 기록.
