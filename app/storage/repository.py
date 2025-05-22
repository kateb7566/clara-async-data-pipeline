from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.schema import RecordModel
from app.utils.logger import get_logger
import redis.asyncio as redis
import json

logger = get_logger(__name__)

class Storage:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url, decode_responses=True)
    
    async def save_to_db(self, data: dict, db: AsyncSession) -> None:
        try:
            record = RecordModel(
                id=int(data["id"]),
                name=data["name"],
                value=data["value"],
                timestamp=data["timestamp"]
            )
            await db.add(record)
            await db.commit()
            logger.info(f"Record {record.id} saved to DB")
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Database error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    async def cache_to_redis(self, data: dict) -> None:
        try:
            await self.redis.rpush("records", str(data))
            logger.info("Record pushed to Redis")
        except Exception as e:
            logger.error(f"Failed to push to Redis: {e}")
            
    async def get_cached_record(self, record_id: int) -> dict:
        try:
            data = await self.redis.get(f"record:{record_id}")
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Failed to get record from Redis: {e}")
            return None

