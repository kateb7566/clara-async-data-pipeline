from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.schema import Record, RecordModel
from app.storage.database import get_db_session
from sqlalchemy.future import select
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/records", response_model=List[Record])
async def get_records(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(RecordModel))
    records = result.scalars().all()
    logger.info("the list of records have been retrieved!")
    return records

@router.get("/records/{record_id}", response_model=Record)
async def get_record(record_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(RecordModel).where(RecordModel.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        logger.warning(f"Record with ID {record_id} not found")
        raise HTTPException(status_code=404, detail="Record not found")
    logger.info(f"the record with ID {record_id} has been retrieved!")
    return record
