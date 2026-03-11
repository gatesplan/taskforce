import json

from taskforce.l1.schema import Opinion
from taskforce.l2.cost_logger import CostLogger


def test_log_creates_monthly_file(tmp_path):
    cl = CostLogger(log_dir=tmp_path)
    opinions = [
        Opinion(model_name="A", content="a", cost=0.05, tokens=500),
        Opinion(model_name="B", content="b", cost=0.03, tokens=300),
    ]
    cl.log("test agenda", opinions, summarizer_cost=0.01, summarizer_tokens=100)

    files = list(tmp_path.glob("*.jsonl"))
    assert len(files) == 1

    record = json.loads(files[0].read_text(encoding="utf-8").strip())
    assert record["total_cost"] == 0.09
    assert record["total_tokens"] == 900
    assert len(record["models"]) == 2


def test_log_appends(tmp_path):
    cl = CostLogger(log_dir=tmp_path)
    opinions = [Opinion(model_name="A", content="a", cost=0.01, tokens=100)]
    cl.log("agenda1", opinions)
    cl.log("agenda2", opinions)

    files = list(tmp_path.glob("*.jsonl"))
    lines = files[0].read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2
