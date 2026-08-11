from __future__ import annotations

import logging
from datetime import UTC, datetime

from datapulse.analytics import (
    calculate_daily_counts,
    calculate_kpis,
    calculate_magnitude_distribution,
    calculate_regional_activity,
)
from datapulse.anomaly import detect_activity_anomaly
from datapulse.database import (
    DEFAULT_DB_PATH,
    get_daily_event_counts,
    get_event_count,
    insert_earthquakes,
)
from datapulse.ingestion import fetch_earthquakes
from datapulse.reporting import generate_daily_report
from datapulse.validation import (
    clean_earthquake_data,
    validate_earthquake_data,
)

logger = logging.getLogger(__name__)


def run_pipeline() -> dict:
    """Execute one complete DataPulse pipeline run."""

    started_at = datetime.now(UTC)

    logger.info("DataPulse pipeline started")

    # 1. Ingest
    raw_df = fetch_earthquakes(days=1)
    logger.info("Fetched %d records", len(raw_df))

    # 2. Validate
    validate_earthquake_data(raw_df)

    # 3. Transform
    clean_df = clean_earthquake_data(raw_df)

    # 4. Persist
    inserted = insert_earthquakes(
        clean_df,
        db_path=DEFAULT_DB_PATH,
    )

    logger.info("Inserted %d new records", inserted)

    # 5. Analytics
    kpis = calculate_kpis(clean_df)
    distribution = calculate_magnitude_distribution(clean_df)
    regional_activity = calculate_regional_activity(clean_df)

    # 6. Historical anomaly detection
    historical_daily_counts = get_daily_event_counts(
        db_path=DEFAULT_DB_PATH,
    )

    daily_counts = calculate_daily_counts(
        historical_daily_counts,
    )

    anomaly = detect_activity_anomaly(daily_counts)

    # 7. Database status
    total_stored = get_event_count(DEFAULT_DB_PATH)

    finished_at = datetime.now(UTC)

    # 8. Build pipeline result
    result = {
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "records_fetched": len(raw_df),
        "records_inserted": inserted,
        "total_records_stored": total_stored,
        "kpis": kpis,
        "distribution": distribution,
        "regional_activity": regional_activity,
        "anomaly": anomaly,
    }

    # 9. Generate daily intelligence report
    report_path = generate_daily_report(result)

    logger.info("Report generated: %s", report_path)

    logger.info(
        "Pipeline completed: fetched=%d inserted=%d stored=%d",
        len(raw_df),
        inserted,
        total_stored,
    )

    return result


def main() -> None:
    """CLI entry point for DataPulse."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    result = run_pipeline()

    print("\nDataPulse Pipeline Complete")
    print("=" * 32)
    print(f"Records fetched: {result['records_fetched']}")
    print(f"Records inserted: {result['records_inserted']}")
    print(f"Total stored: {result['total_records_stored']}")
    print(f"Anomaly status: {result['anomaly']['status']}")
    print(f"Z-score: {result['anomaly']['z_score']}")


if __name__ == "__main__":
    main()