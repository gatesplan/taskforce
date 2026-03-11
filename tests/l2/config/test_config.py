import os

import pytest

from taskforce.l2.config import EnvConfig


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    # 테스트 간 환경변수 격리
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("XAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)


def test_panels_exclude_caller(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("XAI_API_KEY", "xai-test")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "ant-test")

    config = EnvConfig(caller_provider="anthropic", dotenv_path="/dev/null")
    names = [m.display_name for m in config.get_active_panels()]
    assert "Claude opus-4" not in names
    assert "GPT 5.4" in names
    assert "Grok 4-1" in names


def test_no_active_panels_raises(monkeypatch):
    monkeypatch.setenv("XAI_API_KEY", "xai-test")
    with pytest.raises(ValueError, match="활성 패널"):
        EnvConfig(caller_provider="xai", dotenv_path="/dev/null")


def test_no_xai_key_raises(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    with pytest.raises(ValueError, match="XAI_API_KEY"):
        EnvConfig(caller_provider="anthropic", dotenv_path="/dev/null")


def test_summarizer_uses_xai_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("XAI_API_KEY", "xai-test")

    config = EnvConfig(caller_provider="anthropic", dotenv_path="/dev/null")
    assert config.summarizer_model.api_key == "xai-test"
    assert "non-reasoning" in config.summarizer_model.model_id
