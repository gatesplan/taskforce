# l1

## schema
ModelEntry(provider: str, model_id: str, api_key: str, display_name: str)
Opinion(model_name: str, content: str)
DivergentPoint(topic: str, positions: dict[str, str])
UniquePoint(point: str, source_model: str)
IdeaPool(agenda: str, common: list[str], divergent: list[DivergentPoint], unique: list[UniquePoint])
