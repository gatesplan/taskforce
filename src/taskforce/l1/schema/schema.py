from pydantic import BaseModel


class ModelEntry(BaseModel):
    provider: str
    model_id: str
    api_key: str
    display_name: str
    extra_params: dict = {}


class Opinion(BaseModel):
    model_name: str
    content: str
    cost: float = 0.0
    tokens: int = 0


class DivergentPoint(BaseModel):
    topic: str
    positions: dict[str, str]


class UniquePoint(BaseModel):
    point: str
    source_model: str


class IdeaPool(BaseModel):
    agenda: str
    common: list[str]
    divergent: list[DivergentPoint]
    unique: list[UniquePoint]
    total_cost: float = 0.0
    total_tokens: int = 0
