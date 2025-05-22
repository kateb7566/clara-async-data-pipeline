import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from app.storage.repository import Storage
from app.models.schema import RecordModel
from unittest.mock import AsyncMock, patch
import json

@pytest.mark.asyncio
async def test_save_to_db_success():
    # Arrange
    db = AsyncMock()
    storage = Storage()
    data = {
        "id": 1,
        "name": "test_record",
        "value": 100,
        "timestamp": "2024-01-01T00:00:00"
    }

    # Act
    await storage.save_to_db(data, db)

    # Assert
    assert db.add.await_count == 1
    assert db.commit.await_count == 1


@pytest.mark.asyncio
async def test_save_to_db_sqlalchemy_error(caplog):
    # Arrange
    db = AsyncMock()
    db.commit.side_effect = SQLAlchemyError("DB error")
    storage = Storage()
    data = {
        "id": 2,
        "name": "fail_record",
        "value": 200,
        "timestamp": "2024-01-01T00:00:00"
    }

    # Act
    await storage.save_to_db(data, db)

    # Assert
    assert db.rollback.await_count == 1
    assert "Database error" in caplog.text


@pytest.mark.asyncio
async def test_save_to_db_unexpected_error(caplog):
    # Arrange
    db = AsyncMock()
    storage = Storage()
    data = {
        "id": "invalid",  # should raise a ValueError when casting to int
        "name": "oops",
        "value": 123,
        "timestamp": "2024-01-01T00:00:00"
    }

    # Act
    await storage.save_to_db(data, db)

    # Assert
    assert "Unexpected error" in caplog.text
    assert db.commit.await_count == 0
    assert db.rollback.await_count == 0  # didn't even get to commit stage

@pytest.mark.asyncio
async def test_cache_to_redis_success():
    storage = Storage()
    storage.redis = AsyncMock()
    
    test_data = {"id": 1, "name": "test", "value": 10, "timestamp": "2024-01-01T00:00:00"}
    await storage.cache_to_redis(test_data)

    storage.redis.rpush.assert_awaited_with("records", str(test_data))

@pytest.mark.asyncio
async def test_cache_to_redis_failure(caplog):
    storage = Storage()
    storage.redis = AsyncMock()
    storage.redis.rpush.side_effect = Exception("Redis down")

    test_data = {"id": 1, "name": "test", "value": 10, "timestamp": "2024-01-01T00:00:00"}
    await storage.cache_to_redis(test_data)

    assert "Failed to push to Redis" in caplog.text

@pytest.mark.asyncio
async def test_get_cached_record_success():
    storage = Storage()
    storage.redis = AsyncMock()
    
    mock_data = {"id": 1, "name": "cached", "value": 5, "timestamp": "2024-01-01T00:00:00"}
    storage.redis.get.return_value = json.dumps(mock_data)

    result = await storage.get_cached_record(1)
    assert result == mock_data
    storage.redis.get.assert_awaited_with("record:1")

@pytest.mark.asyncio
async def test_get_cached_record_not_found():
    storage = Storage()
    storage.redis = AsyncMock()
    storage.redis.get.return_value = None

    result = await storage.get_cached_record(99)
    assert result is None

@pytest.mark.asyncio
async def test_get_cached_record_failure(caplog):
    storage = Storage()
    storage.redis = AsyncMock()
    storage.redis.get.side_effect = Exception("Connection error")

    result = await storage.get_cached_record(1)
    assert result is None
    assert "Failed to get record from Redis" in caplog.text
