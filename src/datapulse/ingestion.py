from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pandas as pd
import requests


USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


class IngestionError(RuntimeError):
    """Raised when the upstream data source cannot be retrieved or parsed."""


def fetch_earthquakes(
    days: int = 1,
    min_magnitude: float = 0.0,
    timeout: int = 30,
) -> pd.DataFrame:
    """Fetch recent earthquake events from the USGS API.

    Args:
        days: Number of previous days to retrieve.
        min_magnitude: Minimum earthquake magnitude.
        timeout: HTTP request timeout in seconds.

    Returns:
        A DataFrame containing raw earthquake event data.

    Raises:
        IngestionError: If the API request or response parsing fails.
    """
    if days < 1:
        raise ValueError("days must be at least 1")

    if min_magnitude < 0:
        raise ValueError("min_magnitude cannot be negative")

    params = {
        "format": "geojson",
        "starttime": _start_time(days),
        "endtime": datetime.now(UTC).isoformat(),
        "minmagnitude": min_magnitude,
        "orderby": "time-asc",
    }

    try:
        response = requests.get(
            USGS_API_URL,
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
    except requests.RequestException as exc:
        raise IngestionError(f"USGS API request failed: {exc}") from exc
    except ValueError as exc:
        raise IngestionError("USGS API returned invalid JSON") from exc

    features = payload.get("features", [])

    if not isinstance(features, list):
        raise IngestionError("Unexpected USGS API response structure")

    return _features_to_dataframe(features)


def _start_time(days: int) -> str:
    """Return the UTC start timestamp for the requested lookback period."""
    from datetime import timedelta

    return (datetime.now(UTC) - timedelta(days=days)).isoformat()


def _features_to_dataframe(features: list[dict[str, Any]]) -> pd.DataFrame:
    """Convert USGS GeoJSON features into a tabular DataFrame."""
    records: list[dict[str, Any]] = []

    for feature in features:
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        coordinates = geometry.get("coordinates", [])

        if len(coordinates) < 3:
            continue

        records.append(
            {
                "event_id": feature.get("id"),
                "event_time": properties.get("time"),
                "magnitude": properties.get("mag"),
                "place": properties.get("place"),
                "longitude": coordinates[0],
                "latitude": coordinates[1],
                "depth_km": coordinates[2],
                "event_url": properties.get("url"),
                "event_type": properties.get("type"),
            }
        )

    columns = [
        "event_id",
        "event_time",
        "magnitude",
        "place",
        "longitude",
        "latitude",
        "depth_km",
        "event_url",
        "event_type",
    ]

    return pd.DataFrame(records, columns=columns)