import json
from unittest.mock import AsyncMock

import pytest

from taskforce.l1.schema import Opinion, IdeaPool


@pytest.fixture
def _env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("XAI_API_KEY", "xai-test")


def test_taskforce_init(_env):
    from taskforce import Taskforce
    tf = Taskforce(caller_provider="anthropic", dotenv_path="/dev/null")
    assert len(tf.roundtable.panelists) == 2


@pytest.mark.asyncio
async def test_taskforce_discuss(_env, tmp_path):
    from taskforce import Taskforce
    tf = Taskforce(caller_provider="anthropic", dotenv_path="/dev/null")
    tf.session_logger.log_dir = tmp_path / "logs"
    tf.session_logger.log_dir.mkdir()
    tf.cost_logger.log_dir = tmp_path / "cost_logs"
    tf.cost_logger.log_dir.mkdir()

    # 패널 mock
    for p in tf.roundtable.panelists:
        p.ask_async = AsyncMock(
            return_value=Opinion(
                model_name=p.model_entry.display_name,
                content="test opinion",
                cost=0.01,
                tokens=100,
            )
        )

    # summarizer mock
    summary = json.dumps({"common": ["p1"], "divergent": [], "unique": []})
    tf.roundtable.summarizer.ask_async = AsyncMock(
        return_value=Opinion(model_name="S", content=summary, cost=0.005, tokens=50)
    )

    pool = await tf.discuss_async("test agenda")
    assert isinstance(pool, IdeaPool)
    assert pool.common == ["p1"]
    assert pool.total_cost > 0

    # 로그 파일 생성 확인
    assert list((tmp_path / "logs").glob("*.jsonl"))
    assert list((tmp_path / "cost_logs").glob("*.jsonl"))
