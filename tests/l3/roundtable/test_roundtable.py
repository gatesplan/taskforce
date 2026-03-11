import json
from unittest.mock import AsyncMock

import pytest

from taskforce.l1.schema import ModelEntry, Opinion
from taskforce.l2.panelist import Panelist
from taskforce.l3.roundtable import Roundtable


def _make_panelist(name: str) -> Panelist:
    entry = ModelEntry(
        provider="test",
        model_id=f"test-{name}",
        api_key="test-key",
        display_name=name,
    )
    return Panelist(entry)


def _make_summarizer_response(common, divergent, unique) -> str:
    return json.dumps({
        "common": common,
        "divergent": divergent,
        "unique": unique,
    })


@pytest.mark.asyncio
async def test_gather_collects_opinions():
    p1 = _make_panelist("A")
    p2 = _make_panelist("B")
    p1.ask_async = AsyncMock(return_value=Opinion(model_name="A", content="opinion A"))
    p2.ask_async = AsyncMock(return_value=Opinion(model_name="B", content="opinion B"))

    summarizer = _make_panelist("S")
    rt = Roundtable([p1, p2], summarizer)

    opinions = await rt.gather("test agenda")
    assert len(opinions) == 2


@pytest.mark.asyncio
async def test_gather_skips_failed_panelist():
    p1 = _make_panelist("A")
    p2 = _make_panelist("B")
    p1.ask_async = AsyncMock(return_value=Opinion(model_name="A", content="opinion A"))
    p2.ask_async = AsyncMock(side_effect=Exception("fail"))

    summarizer = _make_panelist("S")
    rt = Roundtable([p1, p2], summarizer)

    opinions = await rt.gather("test agenda")
    assert len(opinions) == 1
    assert opinions[0].model_name == "A"


@pytest.mark.asyncio
async def test_discuss_returns_pool_and_opinions():
    p1 = _make_panelist("A")
    p1.ask_async = AsyncMock(return_value=Opinion(model_name="A", content="opinion A", cost=0.01, tokens=100))

    summarizer = _make_panelist("S")
    summary_json = _make_summarizer_response(
        common=["shared point"],
        divergent=[{"topic": "t1", "positions": {"A": "yes"}}],
        unique=[{"point": "insight", "source_model": "A"}],
    )
    summarizer.ask_async = AsyncMock(
        return_value=Opinion(model_name="S", content=summary_json, cost=0.005, tokens=50)
    )

    rt = Roundtable([p1], summarizer)
    pool, opinions = await rt.discuss("test agenda")

    assert pool.agenda == "test agenda"
    assert pool.common == ["shared point"]
    assert len(pool.divergent) == 1
    assert len(pool.unique) == 1
    assert pool.total_cost == 0.015
    assert pool.total_tokens == 150
    assert len(opinions) == 1


@pytest.mark.asyncio
async def test_discuss_empty_when_all_fail():
    p1 = _make_panelist("A")
    p1.ask_async = AsyncMock(side_effect=Exception("fail"))

    summarizer = _make_panelist("S")
    rt = Roundtable([p1], summarizer)

    pool, opinions = await rt.discuss("test agenda")
    assert pool.common == []
    assert opinions == []


@pytest.mark.asyncio
async def test_extract_json_from_markdown_block():
    p1 = _make_panelist("A")
    p1.ask_async = AsyncMock(return_value=Opinion(model_name="A", content="opinion"))

    summarizer = _make_panelist("S")
    wrapped = '```json\n{"common": ["p1"], "divergent": [], "unique": []}\n```'
    summarizer.ask_async = AsyncMock(
        return_value=Opinion(model_name="S", content=wrapped)
    )

    rt = Roundtable([p1], summarizer)
    pool, _ = await rt.discuss("test")
    assert pool.common == ["p1"]
