from taskforce.l1.schema import ModelEntry, Opinion, DivergentPoint, UniquePoint, IdeaPool


def test_model_entry_creation():
    entry = ModelEntry(
        provider="openai",
        model_id="gpt-5.4",
        api_key="sk-test",
        display_name="GPT 5.4",
    )
    assert entry.provider == "openai"
    assert entry.model_id == "gpt-5.4"


def test_opinion_creation():
    op = Opinion(model_name="GPT 5.4", content="test content")
    assert op.model_name == "GPT 5.4"


def test_idea_pool_creation():
    pool = IdeaPool(
        agenda="test agenda",
        common=["point1"],
        divergent=[DivergentPoint(topic="t1", positions={"A": "yes", "B": "no"})],
        unique=[UniquePoint(point="insight", source_model="A")],
    )
    assert pool.agenda == "test agenda"
    assert len(pool.common) == 1
    assert len(pool.divergent) == 1
    assert len(pool.unique) == 1


def test_idea_pool_json_roundtrip():
    pool = IdeaPool(
        agenda="test",
        common=["a", "b"],
        divergent=[],
        unique=[],
    )
    json_str = pool.model_dump_json()
    restored = IdeaPool.model_validate_json(json_str)
    assert restored.agenda == "test"
    assert restored.common == ["a", "b"]
