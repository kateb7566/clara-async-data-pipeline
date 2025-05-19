# transformer.py Transform Data

from typing import Any, List, Dict
from datetime import datetime
from app.utils import get_logger

logger = get_logger()

class Transformer:
    """
    Transforms and cleans raw data for downstream processing.
    """

    def __init__(self):
        pass

    def transform(self, raw_data: Any) -> List[Dict[str, Any]]:
        """
        Main method to process raw data into clean structured form.

        :param raw_data: Raw data fetched from external source
        :return: List of validated and structured data
        """
        if not raw_data:
            logger.warning("Transformer received empty data.")
            return []

        transformed = []

        for item in raw_data:
            try:
                structured = {
                    "id": str(item.get("id")),
                    "name": item.get("name", "").strip(),
                    "timestamp": self.parse_datetime(item.get("timestamp")),
                    "value": float(item.get("value", 0)),
                }

                if self.is_valid(structured):
                    transformed.append(structured)
                else:
                    logger.warning(f"Invalid item skipped: {structured}")

            except Exception as e:
                logger.exception(f"Error transforming item: {item}, Error: {e}")

        return transformed

    def parse_datetime(self, value: str) -> str:
        """
        Converts a timestamp string to a standard ISO format.

        :param value: Raw timestamp
        :return: ISO formatted string
        """
        try:
            dt = datetime.fromisoformat(value)
            return dt.isoformat()
        except Exception:
            logger.warning(f"Invalid datetime: {value}. Using fallback.")
            return datetime.utcnow().isoformat()

    def is_valid(self, item: Dict[str, Any]) -> bool:
        """
        Validates the cleaned item structure.

        :param item: Transformed dictionary
        :return: Boolean indicating validity
        """
        return bool(item["id"] and item["name"] and item["timestamp"])
