from __future__ import annotations

import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict[str, float | int | str | None]:
    """Calculate core earthquake activity KPIs."""
    if df.empty:
        return {
            "total_events": 0,
            "average_magnitude": None,
            "median_magnitude": None,
            "maximum_magnitude": None,
            "minimum_magnitude": None,
        }

    return {
        "total_events": int(len(df)),
        "average_magnitude": round(float(df["magnitude"].mean()), 3),
        "median_magnitude": round(float(df["magnitude"].median()), 3),
        "maximum_magnitude": round(float(df["magnitude"].max()), 3),
        "minimum_magnitude": round(float(df["magnitude"].min()), 3),
    }


def calculate_magnitude_distribution(
    df: pd.DataFrame,
) -> dict[str, int]:
    """Count events by magnitude category."""
    distribution = (
        df["magnitude_category"]
        .value_counts()
        .reindex(
            ["Minor", "Moderate", "Strong", "Major"],
            fill_value=0,
        )
    )

    return {
        category: int(count)
        for category, count in distribution.items()
    }


def calculate_daily_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily earthquake event counts."""
    result = (
        df.groupby("event_date")
        .size()
        .reset_index(name="event_count")
        .sort_values("event_date")
    )

    result["rolling_7d"] = (
        result["event_count"]
        .rolling(window=7, min_periods=1)
        .mean()
        .round(2)
    )

    result["rolling_30d"] = (
        result["event_count"]
        .rolling(window=30, min_periods=1)
        .mean()
        .round(2)
    )

    return result


def calculate_regional_activity(
    df: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return the most active earthquake locations."""
    return (
        df.groupby("place")
        .agg(
            event_count=("event_id", "count"),
            average_magnitude=("magnitude", "mean"),
            maximum_magnitude=("magnitude", "max"),
        )
        .sort_values(
            ["event_count", "maximum_magnitude"],
            ascending=False,
        )
        .head(top_n)
        .reset_index()
    )