import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.ingestion.fetcher import Fetcher

@pytest.mark.asyncio
async def test_fetch_success():
    # Mock response with expected data
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"id": 1, "name": "test"}

    # Use MagicMock for the session, since we need to control get()'s async context behavior
    mock_session = MagicMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response
    mock_session.get.return_value.__aexit__.return_value = None

    fetcher = Fetcher()
    data = await fetcher.fetch(mock_session)

    assert data == {"id": 1, "name": "test"}


@pytest.mark.asyncio
async def test_fetch_non_200():
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.json.return_value = {}

    mock_session = AsyncMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response

    fetcher = Fetcher()
    result = await fetcher.fetch(mock_session)

    assert result is None

@pytest.mark.asyncio
async def test_fetch_raises_exception_then_fails(monkeypatch):
    mock_session = AsyncMock()
    mock_session.get.side_effect = Exception("Connection error")

    fetcher = Fetcher()
    fetcher.retries = 2
    fetcher.retry_backoff = 0  # avoid delay in test

    result = await fetcher.fetch(mock_session)
    assert result is None
