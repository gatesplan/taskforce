# Schema

pydantic 데이터 모델 정의.

## ModelEntry

LLM 프로바이더 모델 정보.

### Properties
provider: str              # 프로바이더명 (openai, xai, anthropic, gemini)
model_id: str              # LiteLLM 모델 ID
api_key: str               # API 키
display_name: str          # 표시용 이름

## Opinion

패널리스트 응답.

### Properties
model_name: str            # 응답한 모델 표시명
content: str               # 응답 전문

## DivergentPoint

모델 간 의견이 갈리는 지점.

### Properties
topic: str                 # 쟁점
positions: dict[str, str]  # {model_name: 해당 입장}

## UniquePoint

한 모델만 제시한 고유 관점.

### Properties
point: str                 # 고유 관점 내용
source_model: str          # 제시한 모델명

## IdeaPool

라운드테이블 결과. 구조화된 아이디어 풀.

### Properties
agenda: str                        # 원본 의제
common: list[str]                  # 다수 모델 공통 포인트
divergent: list[DivergentPoint]    # 이견 지점
unique: list[UniquePoint]          # 고유 관점
