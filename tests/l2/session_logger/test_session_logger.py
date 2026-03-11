import json

from taskforce.l1.schema import Opinion
from taskforce.l2.session_logger import SessionLogger


def test_log_creates_file(tmp_path):
    sl = SessionLogger(log_dir=tmp_path)
    opinions = [
        Opinion(model_name="A", content="opinion A", cost=0.01, tokens=100),
        Opinion(model_name="B", content="opinion B", cost=0.02, tokens=200),
    ]
    filepath = sl.log("test agenda", "test context", opinions)
    assert filepath.exists()

    lines = filepath.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 3

    request = json.loads(lines[0])
    assert request["type"] == "request"
    assert request["agenda"] == "test agenda"

    op1 = json.loads(lines[1])
    assert op1["type"] == "opinion"
    assert op1["model_name"] == "A"


def test_log_includes_summarizer(tmp_path):
    sl = SessionLogger(log_dir=tmp_path)
    opinions = [Opinion(model_name="A", content="opinion A")]
    filepath = sl.log("agenda", "", opinions, summarizer_output="summary text")

    lines = filepath.read_text(encoding="utf-8").strip().split("\n")
    last = json.loads(lines[-1])
    assert last["type"] == "summarizer"
    assert last["content"] == "summary text"
