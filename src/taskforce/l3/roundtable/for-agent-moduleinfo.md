# Roundtable

병렬 패널 질의 + summarizer 분류 취합.

## Roundtable

다수 패널리스트에 의제를 병렬 질의하고 summarizer로 분류.

### Properties
panelists: list[Panelist]  # 패널 모델 목록
summarizer: Panelist       # 분류 취합용 모델

### __init__
__init__(panelists: list[Panelist], summarizer: Panelist)
    패널과 summarizer 설정.

### Methods

gather(agenda: str, context: str = "") -> list[Opinion]
    asyncio.gather로 전체 패널 병렬 질의.
    실패한 패널은 제외, 성공분만 반환.

summarize(agenda: str, opinions: list[Opinion]) -> IdeaPool
    raise ValueError
    opinions를 summarizer에 전달하여 common/divergent/unique 분류.
    JSON 파싱 실패 시 ValueError.

discuss(agenda: str, context: str = "") -> IdeaPool
    gather + summarize 일괄 실행.
    의견 0개이면 빈 IdeaPool 반환.
