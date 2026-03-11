# SessionLogger

세션 전문 로그 기록. prompt, response 원문을 JSONL로 저장.

## SessionLogger

~/.taskforce/logs/ 에 세션별 JSONL 파일 생성.

### Properties
log_dir: Path              # 로그 디렉토리 경로

### __init__
__init__(log_dir: Path | None = None)
    log_dir 미지정 시 ~/.taskforce/logs/ 사용.
    디렉토리 자동 생성.

### Methods

log(agenda: str, context: str, opinions: list[Opinion], summarizer_output: str = "") -> Path
    세션 로그 파일 생성.
    request, opinion, summarizer 레코드를 JSONL로 기록.
    생성된 파일 경로 반환.
