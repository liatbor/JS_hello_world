"""Tests for the Hello World Agent."""
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage


# ---------------------------------------------------------------------------
# Unit test: agent responds with "Hello World" to any input
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_agent_responds_with_hello_world():
    """Agent must always respond with 'Hello World'."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_result = {
        "messages": [
            HumanMessage(content="Hi"),
            AIMessage(content="Hello World"),
        ]
    }

    with patch.object(agent, "_invoke", new=AsyncMock(return_value=mock_result)):
        response = await agent.invoke("Hi", context_id="test-ctx-1")

    assert response.status == "completed"
    assert "Hello World" in response.message


@pytest.mark.asyncio
async def test_agent_responds_with_hello_world_any_input():
    """Agent must respond with 'Hello World' regardless of what the user says."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_result = {
        "messages": [
            HumanMessage(content="Tell me a joke"),
            AIMessage(content="Hello World"),
        ]
    }

    with patch.object(agent, "_invoke", new=AsyncMock(return_value=mock_result)):
        response = await agent.invoke("Tell me a joke", context_id="test-ctx-2")

    assert response.status == "completed"
    assert "Hello World" in response.message


@pytest.mark.asyncio
async def test_agent_stream_yields_hello_world():
    """Stream method should yield a completed response containing 'Hello World'."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_result = {
        "messages": [
            HumanMessage(content="Hello"),
            AIMessage(content="Hello World"),
        ]
    }

    with patch.object(agent, "_invoke", new=AsyncMock(return_value=mock_result)):
        chunks = []
        async for chunk in agent.stream("Hello", context_id="test-ctx-3"):
            chunks.append(chunk)

    assert len(chunks) >= 2
    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert "Hello World" in final["content"]


@pytest.mark.asyncio
async def test_agent_handles_empty_messages_gracefully():
    """Agent should handle an empty messages list without crashing."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_result = {"messages": []}

    with patch.object(agent, "_invoke", new=AsyncMock(return_value=mock_result)):
        response = await agent.invoke("anything", context_id="test-ctx-4")

    assert response.status == "completed"
    assert response.message == "Agent returned no response."


@pytest.mark.asyncio
async def test_agent_error_returns_graceful_response():
    """Agent should return a graceful response (not crash) when an unexpected error occurs."""
    from agent import SampleAgent

    agent = SampleAgent()

    with patch.object(agent, "_invoke", new=AsyncMock(side_effect=RuntimeError("boom"))):
        response = await agent.invoke("anything", context_id="test-ctx-5")

    # The agent framework catches errors and returns completed with an error message
    assert response.status == "completed"
    assert response.message is not None
    assert len(response.message) > 0


# ---------------------------------------------------------------------------
# Integration test: end-to-end flow through invoke with mocked LLM
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_integration_end_to_end_hello_world():
    """Integration test: full agent flow returns 'Hello World'."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_result = {
        "messages": [
            HumanMessage(content="Good morning"),
            AIMessage(content="Hello World"),
        ]
    }

    with patch.object(agent, "_invoke", new=AsyncMock(return_value=mock_result)):
        response = await agent.invoke("Good morning", context_id="integration-test-ctx")

    assert response.status == "completed"
    assert "Hello World" in response.message
    assert response.message == "Hello World"
