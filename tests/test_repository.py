import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock

from app.storage.repository import Storage

@pytest.mark.asyncio
async def test_storage_save_success():
    sample_data = {"id": 1, "value": "test"}

    with patch("os.makedirs") as mock_makedirs, \
        patch("aiofiles.open", new_callable=AsyncMock) as mock_open:
        
        # Set up the async context manager mock
        mock_file = AsyncMock()
        mock_open.return_value.__aenter__.return_value = mock_file

        storage = Storage()
        await storage.save(sample_data)

        # Check file was opened in append mode
        mock_open.assert_called_once()
        
        # Check that json data was written properly
        written_data = json.dumps(sample_data) + "\n"
        mock_file.write.assert_awaited_once_with(written_data)
