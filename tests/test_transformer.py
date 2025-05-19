import pytest
from app.transformation.transformer import Transformer
from datetime import datetime

@pytest.fixture
def transformer():
    return Transformer()

def test_transform_valid_data(transformer):
    raw_data = [
        {"id": 1, "name": " Test ", "timestamp": "2024-01-01T10:00:00", "value": "12.5"},
    ]

    result = transformer.transform(raw_data)

    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert result[0]["name"] == "Test"
    assert result[0]["timestamp"] == "2024-01-01T10:00:00"
    assert result[0]["value"] == 12.5

def test_transform_invalid_data_skips(transformer):
    raw_data = [
        {"id": None, "name": "", "timestamp": "bad-format", "value": "NaN"},
    ]

    result = transformer.transform(raw_data)

    assert result == []  # No valid entries

def test_transform_partial_data(transformer):
    raw_data = [
        {"id": 5, "name": "Foo", "timestamp": None},  # Missing timestamp
    ]

    result = transformer.transform(raw_data)
    assert len(result) == 1
    assert "timestamp" in result[0]
    # It should have fallback datetime
    assert isinstance(result[0]["timestamp"], str)

def test_transform_empty_data(transformer):
    result = transformer.transform([])
    assert result == []

    result_none = transformer.transform(None)
    assert result_none == []
