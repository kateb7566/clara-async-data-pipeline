import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.main import app  # assuming your FastAPI app is here
from app.models.schema import RecordModel
from app.storage.database import get_db_session

# Test DB override setup
@pytest.fixture
async def test_db_session(async_session: AsyncSession):
    yield async_session  # this should be a clean test session (fixture defined elsewhere)

@pytest.fixture(autouse=True)
def override_get_db_session(test_db_session):
    app.dependency_overrides[get_db_session] = lambda: test_db_session

@pytest.mark.asyncio
async def test_get_records_empty(async_session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/records")
        assert response.status_code == 200
        assert response.json() == []

@pytest.mark.asyncio
async def test_get_records_with_data(async_session):
    # Insert mock data
    record = RecordModel(id=1, name="Test", timestamp="2024-01-01T00:00:00", value=10.0)
    async_session.add(record)
    await async_session.commit()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/records")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["name"] == "Test"

@pytest.mark.asyncio
async def test_get_record_by_id_found(async_session):
    record = RecordModel(id=2, name="Found", timestamp="2024-01-02T00:00:00", value=20.0)
    async_session.add(record)
    await async_session.commit()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/records/2")
        assert response.status_code == 200
        assert response.json()["name"] == "Found"

@pytest.mark.asyncio
async def test_get_record_by_id_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/records/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Record not found"
