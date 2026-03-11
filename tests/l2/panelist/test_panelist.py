from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from taskforce.l1.schema import ModelEntry
from taskforce.l2.panelist import Panelist


@pytest.fixture
def openai_entry():
    return ModelEntry(
        provider="openai",
        model_id="gpt-5.4",
        api_key="sk-test",
        display_name="GPT 5.4",
    )


@pytest.fixture
def xai_entry():
    return ModelEntry(
        provider="xai",
        model_id="grok-4-1",
        api_key="xai-test",
        display_name="Grok 4-1",
    )


def test_openai_model_id(openai_entry):
    p = Panelist(openai_entry)
    assert p._litellm_model == "gpt-5.4"


def test_xai_model_id(xai_entry):
    p = Panelist(xai_entry)
    assert p._litellm_model == "xai/grok-4-1"


@pytest.mark.asyncio
async def test_ask_async_returns_opinion(openai_entry):
    p = Panelist(openai_entry)

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "test response"

    with patch("litellm.acompletion", new_callable=AsyncMock, return_value=mock_response):
        opinion = await p.ask_async("test prompt")
        assert opinion.model_name == "GPT 5.4"
        assert opinion.content == "test response"


@pytest.mark.asyncio
async def test_ask_async_raises_on_failure(openai_entry):
    p = Panelist(openai_entry)

    with patch("litellm.acompletion", new_callable=AsyncMock, side_effect=Exception("API error")):
        with pytest.raises(Exception, match="API error"):
            await p.ask_async("test prompt")
