from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.schema import Record, RecordModel
from app.storage.database import get_db_session
from sqlalchemy.future import select

router = APIRouter()

@router.get("/records", response_model=List[Record])
async def get_records(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(RecordModel))
    records = result.scalars().all()
    return records

@router.get("/records/{record_id}", response_model=Record)
async def get_record(record_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(RecordModel).where(RecordModel.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
