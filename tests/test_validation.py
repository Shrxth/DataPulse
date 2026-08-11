import pandas as pd
import pytest

from datapulse.validation import (
    ValidationError,
    clean_earthquake_data,
    validate_earthquake_data,
)


def valid_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "event_id": ["event-1", "event-2"],
            "event_time": [1786395821870, 1786395915260],
            "magnitude": [2.5, 4.2],
            "place": ["Test Location 1", "Test Location 2"],
            "longitude": [-116.7, -122.7],
            "latitude": [33.7, 38.8],
            "depth_km": [10.0, 5.0],
            "event_url": ["url-1", "url-2"],
            "event_type": ["earthquake", "earthquake"],
        }
    )


def test_valid_data_passes_validation() -> None:
    df = valid_dataframe()

    validate_earthquake_data(df)


def test_missing_required_column_fails() -> None:
    df = valid_dataframe().drop(columns=["magnitude"])

    with pytest.raises(ValidationError):
        validate_earthquake_data(df)


def test_duplicate_event_ids_fail() -> None:
    df = valid_dataframe()
    df.loc[1, "event_id"] = "event-1"

    with pytest.raises(ValidationError):
        validate_earthquake_data(df)


def test_invalid_latitude_fails() -> None:
    df = valid_dataframe()
    df.loc[0, "latitude"] = 200

    with pytest.raises(ValidationError):
        validate_earthquake_data(df)


def test_cleaning_converts_timestamp() -> None:
    df = valid_dataframe()

    cleaned = clean_earthquake_data(df)

    assert pd.api.types.is_datetime64tz_dtype(cleaned["event_time"])
    assert "magnitude_category" in cleaned.columns
    assert "event_date" in cleaned.columns
    assert "event_hour" in cleaned.columns