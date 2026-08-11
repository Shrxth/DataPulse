from __future__ import annotations

import pandas as pd


def detect_activity_anomaly(
    daily_counts: pd.DataFrame,
    baseline_days: int = 30,
) -> dict[str, float | str | bool]:
    """Detect unusual daily activity using a rolling z-score baseline.

    This detects unusual activity relative to the observed dataset.
    It does not predict earthquakes.
    """
    if daily_counts.empty:
        return {
            "is_anomaly": False,
            "status": "NO_DATA",
            "z_score": 0.0,
            "current_count": 0,
            "baseline_mean": 0.0,
            "baseline_std": 0.0,
        }

    counts = daily_counts["event_count"].astype(float)

    current_count = float(counts.iloc[-1])

    historical = counts.iloc[:-1].tail(baseline_days)

    if len(historical) < 2:
        return {
            "is_anomaly": False,
            "status": "INSUFFICIENT_HISTORY",
            "z_score": 0.0,
            "current_count": current_count,
            "baseline_mean": float(historical.mean())
            if not historical.empty
            else 0.0,
            "baseline_std": float(historical.std())
            if len(historical) > 1
            else 0.0,
        }

    baseline_mean = float(historical.mean())
    baseline_std = float(historical.std())

    if baseline_std == 0:
        z_score = 0.0
    else:
        z_score = (current_count - baseline_mean) / baseline_std

    absolute_z = abs(z_score)

    if absolute_z >= 3:
        status = "ANOMALY"
    elif absolute_z >= 2:
        status = "WARNING"
    else:
        status = "NORMAL"

    return {
        "is_anomaly": status == "ANOMALY",
        "status": status,
        "z_score": round(z_score, 3),
        "current_count": current_count,
        "baseline_mean": round(baseline_mean, 3),
        "baseline_std": round(baseline_std, 3),
    }