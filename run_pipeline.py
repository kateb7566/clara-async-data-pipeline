# call ingestion layer manually

from app.ingestion.fetcher import Fetcher
from app.storage.repository import Storage
from app.utils.logger import get_logger
import asyncio

logger = get_logger()

async def main():
    fetcher = Fetcher()
    storage = Storage()
    
    try:
        logger.info("Starting async data pipeline...")
        data = await fetcher.run()
        if data:
            await storage.save(data)
            logger.info("Data saved successfully.")
        else:
            logger.warning("No data fetched.")
            
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())