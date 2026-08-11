from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path


DEFAULT_REPORT_DIR = Path("reports")


def generate_daily_report(
    result: dict,
    output_dir: Path = DEFAULT_REPORT_DIR,
) -> Path:
    """Generate a Markdown intelligence report for a pipeline run."""
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC)
    report_path = output_dir / f"{timestamp.date().isoformat()}.md"

    kpis = result["kpis"]
    distribution = result["distribution"]
    anomaly = result["anomaly"]
    regional_activity = result["regional_activity"]

    lines = [
        "# DataPulse Daily Intelligence Report",
        "",
        f"**Generated:** {timestamp.isoformat()}",
        "",
        "## Pipeline",
        "",
        f"- Records fetched: {result['records_fetched']}",
        f"- New records inserted: {result['records_inserted']}",
        f"- Total records stored: {result['total_records_stored']}",
        "",
        "## Key Performance Indicators",
        "",
        f"- Total events: {kpis['total_events']}",
        f"- Average magnitude: {kpis['average_magnitude']}",
        f"- Median magnitude: {kpis['median_magnitude']}",
        f"- Maximum magnitude: {kpis['maximum_magnitude']}",
        f"- Minimum magnitude: {kpis['minimum_magnitude']}",
        "",
        "## Magnitude Distribution",
        "",
    ]

    for category, count in distribution.items():
        lines.append(f"- {category}: {count}")

    lines.extend(
        [
            "",
            "## Activity Anomaly",
            "",
            f"- Status: **{anomaly['status']}**",
            f"- Current event count: {anomaly['current_count']}",
            f"- Baseline mean: {anomaly['baseline_mean']}",
            f"- Baseline standard deviation: {anomaly['baseline_std']}",
            f"- Z-score: {anomaly['z_score']}",
            "",
            "> Note: anomaly detection identifies unusual activity relative "
            "to the observed historical baseline. It does not predict earthquakes.",
            "",
            "## Most Active Locations",
            "",
            "| Location | Events | Avg Magnitude | Max Magnitude |",
            "|---|---:|---:|---:|",
        ]
    )

    for row in regional_activity.itertuples(index=False):
        lines.append(
            f"| {row.place} | {row.event_count} | "
            f"{row.average_magnitude:.2f} | {row.maximum_magnitude:.2f} |"
        )

    lines.extend(
        [
            "",
            "## Pipeline Status",
            "",
            "✅ Ingestion completed",
            "✅ Validation completed",
            "✅ Transformation completed",
            "✅ Database update completed",
            "✅ Analytics completed",
            "✅ Anomaly detection completed",
        ]
    )

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return report_path