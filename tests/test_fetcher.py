import pytest
import aiohttp
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from app.ingestion.fetcher import Fetcher

@pytest.mark.asyncio
async def test_fetcher_success_response():
    # Sample mocked API response
    sample_response = {"message": "Success"}

    # Patch the session.get call inside aiohttp.ClientSession
    with patch("aiohttp.ClientSession.get") as mock_get:
        # Mocking the async context manager behavior
        mock_response = MagicMock()
        mock_response.__aenter__.return_value = mock_response
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=sample_response)
        mock_get.return_value = mock_response

        fetcher = Fetcher()
        async with aiohttp.ClientSession() as session:
            result = await fetcher.fetch(session)

        assert result == sample_response
        mock_get.assert_called_once()

@pytest.mark.asyncio
async def test_fetcher_non_200_response():
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = MagicMock()
        mock_response.__aenter__.return_value = mock_response
        mock_response.status = 404
        mock_response.json = AsyncMock(return_value={"error": "Not found"})
        mock_get.return_value = mock_response

        fetcher = Fetcher()
        async with aiohttp.ClientSession() as session:
            result = await fetcher.fetch(session)

        assert result is None

@pytest.mark.asyncio
async def test_fetcher_all_retries_fail():
    with patch("aiohttp.ClientSession.get", side_effect=Exception("Connection failed")):
        fetcher = Fetcher()
        async with aiohttp.ClientSession() as session:
            result = await fetcher.fetch(session)

        assert result is None
