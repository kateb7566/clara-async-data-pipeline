import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from fastapi import HTTPException

from app.api.routes import get_records, get_record
from app.models.schema import RecordModel

# Mock record for reuse
mock_record = RecordModel(
    id=1,
    name="Test Record",
    value=99.9,
    timestamp=datetime(2024, 1, 1, 0, 0)
)

# -------------------------------
# ✅ Use Case: Get all records - Success
# -------------------------------
@pytest.mark.asyncio
async def test_get_all_records_success():
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_record]
    mock_session.execute.return_value = mock_result

    result = await get_records(db=mock_session)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id == mock_record.id
    assert result[0].name == mock_record.name

# -------------------------------
# ✅ Use Case: Get all records - No records found
# -------------------------------
@pytest.mark.asyncio
async def test_get_all_records_empty():
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute.return_value = mock_result

    result = await get_records(db=mock_session)

    assert isinstance(result, list)
    assert result == []

# -------------------------------
# ✅ Use Case: Get record by ID - Success
# -------------------------------
@pytest.mark.asyncio
async def test_get_record_by_id_success():
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_record
    mock_session.execute.return_value = mock_result

    result = await get_record(record_id=1, db=mock_session)

    assert result.id == mock_record.id
    assert result.name == mock_record.name

# -------------------------------
# ✅ Use Case: Get record by ID - Not found
# -------------------------------
@pytest.mark.asyncio
async def test_get_record_by_id_not_found():
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await get_record(record_id=999, db=mock_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Record not found"
