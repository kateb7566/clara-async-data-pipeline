import aiofiles
import os
import json
from datetime import datetime
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger()

class Storage:
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _get_filename(self) -> str:
        date_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"data_{date_str}.jsonl")
    
    async def save(self, data: dict) -> None:
        filename = self._get_filename()
        
        try:
            async with aiofiles.open(filename, mode="a") as f:
                await f.write(json.dumps(data) + "\n")
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")