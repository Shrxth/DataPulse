from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "event_id",
    "event_time",
    "magnitude",
    "place",
    "longitude",
    "latitude",
    "depth_km",
}


class ValidationError(ValueError):
    """Raised when incoming earthquake data fails validation."""


def validate_earthquake_data(df: pd.DataFrame) -> None:
    """Validate the structural and basic numerical integrity of earthquake data."""
    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValidationError(
            f"Missing required columns: {sorted(missing)}"
        )

    if df.empty:
        raise ValidationError("Earthquake dataset is empty")

    if df["event_id"].isna().any():
        raise ValidationError("event_id contains missing values")

    if df["event_id"].duplicated().any():
        raise ValidationError("Duplicate event_id values detected")

    numeric_columns = [
        "magnitude",
        "longitude",
        "latitude",
        "depth_km",
    ]

    for column in numeric_columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValidationError(f"{column} must be numeric")

    if not df["latitude"].between(-90, 90).all():
        raise ValidationError("Latitude outside valid range")

    if not df["longitude"].between(-180, 180).all():
        raise ValidationError("Longitude outside valid range")

    if not df["magnitude"].notna().all():
        raise ValidationError("Magnitude contains missing values")

    if not df["depth_km"].notna().all():
        raise ValidationError("Depth contains missing values")


def clean_earthquake_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize validated earthquake data for downstream processing."""
    cleaned = df.copy()

    cleaned["event_time"] = pd.to_datetime(
        cleaned["event_time"],
        unit="ms",
        utc=True,
        errors="coerce",
    )

    if cleaned["event_time"].isna().any():
        raise ValidationError("Invalid event timestamps detected")

    cleaned["magnitude"] = pd.to_numeric(
        cleaned["magnitude"],
        errors="coerce",
    )

    cleaned["longitude"] = pd.to_numeric(
        cleaned["longitude"],
        errors="coerce",
    )

    cleaned["latitude"] = pd.to_numeric(
        cleaned["latitude"],
        errors="coerce",
    )

    cleaned["depth_km"] = pd.to_numeric(
        cleaned["depth_km"],
        errors="coerce",
    )

    # USGS can report shallow/negative depths for events above
    # the reference surface. Preserve the event while normalizing
    # depth to a physically interpretable non-negative value.
    cleaned["depth_km"] = cleaned["depth_km"].clip(lower=0)

    cleaned["place"] = cleaned["place"].fillna("Unknown location").astype(str)

    cleaned["magnitude_category"] = pd.cut(
        cleaned["magnitude"],
        bins=[-float("inf"), 2.5, 5.0, 7.0, float("inf")],
        labels=["Minor", "Moderate", "Strong", "Major"],
        right=False,
    )

    cleaned["event_date"] = cleaned["event_time"].dt.date
    cleaned["event_hour"] = cleaned["event_time"].dt.hour

    return cleaned.reset_index(drop=True)