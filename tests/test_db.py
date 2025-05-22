import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.storage.database import get_db_session

import pytest
from unittest.mock import AsyncMock, patch
from app.storage.database import get_db_session

@pytest.mark.asyncio
async def test_get_db_session_yields_async_session():
    fake_session = AsyncMock()

    with patch("app.storage.database.AsyncSessionLocal", return_value=AsyncMock(__aenter__=AsyncMock(return_value=fake_session), __aexit__=AsyncMock())):
        gen = get_db_session()
        session = await anext(gen)
        assert session is fake_session
