# Async function to fetch a sample public API (JSONPlaceholder, httpbin, ...)

import aiohttp
import asyncio
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Fetcher:
    def __init__(self):
        self.api_endpoint = settings.API_ENDPOINT
        self.api_key = settings.API_KEY
        self.timeout = aiohttp.ClientTimeout(total=settings.REQUEST_TIMEOUT)
        self.retries = settings.MAX_RETRIES
        self.retry_backoff = settings.RETRY_BACKOFF
        
    async def fetch(self, session: aiohttp.ClientSession) -> dict | None:
        retries = 0
        while retries < self.max_retries:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                async with session.get(self.api_endpoint, headers=headers, timeout=self.timeout) as response:
                    if response.status == 200:
                        logger.info("Data fetched successfully.")
                        return await response.json()
                    else:
                        logger.warning(f"Non-200 response: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Fetch attempt {retries + 1} failed: {e}")
                retries += 1
                await asyncio.sleep(self.retry_backoff * retries)
                
        logger.error("All fetch attempts failed.")
        return None
    
    async def run(self) -> dict | None:
        async with aiohttp.ClientSession as session:
            return await self.fetch(session=session)