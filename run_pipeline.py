# call ingestion layer manually

from app.ingestion.fetcher import Fetcher
from app.storage.repository import Storage
import asyncio

async def main():
    fetcher = Fetcher()
    storage = Storage()
    
    data = await fetcher.run()
    if data:
        await storage.save(data)


if __name__ == "__main__":
    asyncio.run(main())