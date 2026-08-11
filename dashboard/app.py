from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = Path("database") / "datapulse.db"


st.set_page_config(
    page_title="DataPulse",
    page_icon="🌍",
    layout="wide",
)


@st.cache_data(ttl=300)
def load_data() -> pd.DataFrame:
    """Load earthquake data from the DataPulse SQLite database."""
    if not DB_PATH.exists():
        return pd.DataFrame()

    query = """
        SELECT
            event_id,
            event_time,
            magnitude,
            place,
            longitude,
            latitude,
            depth_km,
            magnitude_category,
            event_date
        FROM earthquakes
        ORDER BY event_time
    """

    with sqlite3.connect(DB_PATH) as connection:
        df = pd.read_sql_query(query, connection)

    if not df.empty:
        df["event_time"] = pd.to_datetime(
            df["event_time"],
            format="mixed",
            utc=True,
        )

    return df


st.title("🌍 DataPulse")
st.caption("Automated Data Intelligence Pipeline")


df = load_data()


if df.empty:
    st.warning(
        "No data available yet. Run the DataPulse pipeline first."
    )
    st.stop()


# KPI calculations

total_events = len(df)
average_magnitude = df["magnitude"].mean()
maximum_magnitude = df["magnitude"].max()
latest_event = df["event_time"].max()


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Events",
    f"{total_events:,}",
)


col2.metric(
    "Average Magnitude",
    f"{average_magnitude:.2f}",
)


col3.metric(
    "Maximum Magnitude",
    f"{maximum_magnitude:.2f}",
)


col4.metric(
    "Latest Event",
    latest_event.strftime("%Y-%m-%d %H:%M UTC"),
)


st.divider()


# Event activity over time

daily = (
    df.groupby("event_date")
    .size()
    .reset_index(name="event_count")
)


daily["event_date"] = pd.to_datetime(
    daily["event_date"]
)


fig_activity = px.line(
    daily,
    x="event_date",
    y="event_count",
    markers=True,
    title="Earthquake Activity",
)


st.plotly_chart(
    fig_activity,
    use_container_width=True,
)


# Magnitude distribution

col1, col2 = st.columns(2)


with col1:
    distribution = (
        df["magnitude_category"]
        .value_counts()
        .reindex(
            ["Minor", "Moderate", "Strong", "Major"],
            fill_value=0,
        )
        .reset_index()
    )

    distribution.columns = [
        "category",
        "count",
    ]

    fig_distribution = px.bar(
        distribution,
        x="category",
        y="count",
        title="Magnitude Distribution",
    )

    st.plotly_chart(
        fig_distribution,
        use_container_width=True,
    )


with col2:
    regional = (
        df.groupby("place")
        .size()
        .reset_index(name="event_count")
        .sort_values(
            "event_count",
            ascending=False,
        )
        .head(10)
    )

    fig_regions = px.bar(
        regional,
        x="event_count",
        y="place",
        orientation="h",
        title="Most Active Locations",
    )

    st.plotly_chart(
        fig_regions,
        use_container_width=True,
    )


# Geographic view

st.subheader("Geographic Distribution")


map_data = df[
    [
        "latitude",
        "longitude",
        "magnitude",
        "place",
    ]
].copy()


map_data = map_data.dropna(
    subset=[
        "latitude",
        "longitude",
    ],
)


st.map(
    map_data,
    latitude="latitude",
    longitude="longitude",
)


# Raw data

with st.expander("View Recent Events"):
    st.dataframe(
        df.sort_values(
            "event_time",
            ascending=False,
        ).head(100),
        use_container_width=True,
    )


st.caption(
    "Data source: USGS Earthquake Hazards Program. "
    "Anomaly detection identifies unusual activity relative "
    "to the observed historical baseline and does not predict earthquakes."
)