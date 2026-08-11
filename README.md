# 🌍 DataPulse

> Automated Data Intelligence Pipeline for real-world public data.

DataPulse is an end-to-end data engineering and analytics project that automatically ingests public API data, validates and transforms it, persists it in SQLite, calculates business-style KPIs, detects anomalous activity, generates daily intelligence reports, and publishes the latest results through an interactive Streamlit dashboard.

The entire pipeline is automated with GitHub Actions and can execute without a local machine being online.

---

## 🚀 What DataPulse Does

Every scheduled run performs the following workflow:

```text
Public API
    ↓
Data Ingestion
    ↓
Validation
    ↓
Cleaning & Transformation
    ↓
SQLite Persistence
    ↓
Analytics & KPIs
    ↓
Anomaly Detection
    ↓
Daily Report
    ↓
Streamlit Dashboard
    ↓
Automated Tests + Ruff
    ↓
GitHub Actions
```

### Automated capabilities

- 🌐 Pulls live earthquake data from the USGS API
- 🧹 Validates and cleans incoming records
- 🗄️ Persists data in SQLite
- 📊 Calculates analytical KPIs
- 📈 Tracks activity over time
- 🌎 Analyzes geographic activity
- 🚨 Detects unusual activity against historical baselines
- 📝 Generates daily Markdown intelligence reports
- 📊 Provides an interactive Streamlit dashboard
- 🧪 Runs automated tests
- 🔍 Runs Ruff code-quality checks
- ☁️ Executes automatically through GitHub Actions
- 🔄 Commits generated results back to the repository

---

## 📊 Current KPIs

The pipeline currently calculates:

| KPI | Description |
|---|---|
| Total Events | Number of earthquake events processed |
| Average Magnitude | Mean earthquake magnitude |
| Median Magnitude | Median earthquake magnitude |
| Maximum Magnitude | Highest recorded magnitude |
| Minimum Magnitude | Lowest recorded magnitude |
| Magnitude Distribution | Events grouped by severity |
| Regional Activity | Most active locations |
| Activity Anomaly | Detection of unusual event volumes |

---

## 🧠 Anomaly Detection

DataPulse compares current activity against the available historical baseline.

The system reports:

- Current event count
- Historical mean
- Historical standard deviation
- Z-score
- Anomaly status

Possible states include:

```text
NORMAL
ANOMALY
INSUFFICIENT_HISTORY
```

> DataPulse is an analytical monitoring system. Its anomaly detection does not predict earthquakes or provide geological forecasts.

---

## 📈 Dashboard

DataPulse includes an interactive Streamlit dashboard containing:

- KPI cards
- Earthquake activity trends
- Magnitude distribution
- Most active locations
- Geographic distribution
- Recent event data

Run locally with:

```bash
streamlit run dashboard/app.py
```

---

## ⚙️ Automation

The pipeline is executed through **GitHub Actions** on a scheduled basis.

The workflow:

1. Checks out the repository
2. Installs Python 3.12
3. Installs project dependencies
4. Runs automated tests
5. Runs Ruff
6. Executes the DataPulse pipeline
7. Generates updated reports and data
8. Commits generated changes when required

Manual execution is also supported through GitHub Actions.

---

## 🧪 Testing

The project includes automated tests covering:

- Data validation
- Transformation
- Analytics
- Anomaly detection
- Database operations
- Ingestion

Run the test suite locally:

```bash
python -m pytest
```

Run code-quality checks:

```bash
ruff check .
```

---

## 🗂️ Project Structure

```text
DataPulse/
│
├── .github/
│   └── workflows/
│       └── pipeline.yml
│
├── dashboard/
│   └── app.py
│
├── database/
│   └── datapulse.db
│
├── reports/
│   └── YYYY-MM-DD.md
│
├── src/
│   └── datapulse/
│       ├── analytics.py
│       ├── anomaly.py
│       ├── config.py
│       ├── database.py
│       ├── ingestion.py
│       ├── logging_config.py
│       ├── pipeline.py
│       ├── reporting.py
│       ├── transformation.py
│       └── validation.py
│
├── tests/
│   ├── test_analytics.py
│   ├── test_anomaly.py
│   ├── test_database.py
│   ├── test_ingestion.py
│   ├── test_transformation.py
│   └── test_validation.py
│
├── pyproject.toml
├── .gitignore
└── README.md
```

---

## 🛠️ Technology Stack

### Data Engineering

- Python
- Pandas
- SQLite
- REST APIs
- SQL

### Analytics

- Pandas
- Statistical analysis
- KPI computation
- Anomaly detection

### Visualization

- Streamlit
- Plotly

### Quality & Automation

- Pytest
- Ruff
- Git
- GitHub Actions
- CI/CD

---

## 🌐 Data Source

Data is sourced from the:

**USGS Earthquake Hazards Program**

The project uses publicly available earthquake event data through the USGS API.

---

## 💻 Local Setup

Clone the repository:

```bash
git clone https://github.com/Shrxth/DataPulse.git
cd DataPulse
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run the pipeline:

```bash
python -m datapulse.pipeline
```

Launch the dashboard:

```bash
streamlit run dashboard/app.py
```

---

## 🔮 Roadmap

DataPulse is intentionally designed to evolve beyond the current SQLite-based MVP.

### Phase 1 — Foundation

- [x] API ingestion
- [x] Data validation
- [x] Data transformation
- [x] SQLite persistence
- [x] KPI analytics
- [x] Anomaly detection
- [x] Daily reporting
- [x] Streamlit dashboard
- [x] Automated testing
- [x] Ruff quality checks
- [x] GitHub Actions automation

### Phase 2 — Production Data Architecture

- [ ] PostgreSQL/Supabase persistence
- [ ] Incremental ingestion
- [ ] Better historical baselines
- [ ] Data quality monitoring
- [ ] Retry and failure handling
- [ ] Structured pipeline logging

### Phase 3 — Advanced Intelligence

- [ ] Multi-source data ingestion
- [ ] Automated anomaly explanations
- [ ] Statistical forecasting
- [ ] ML-based anomaly detection
- [ ] Natural-language intelligence summaries
- [ ] Automated alerts

### Phase 4 — Production Deployment

- [ ] Cloud-hosted dashboard
- [ ] Containerized deployment
- [ ] Secrets management
- [ ] Monitoring
- [ ] Observability
- [ ] Production database
- [ ] Infrastructure automation

---

## 🎯 Why This Project Exists

DataPulse is designed to demonstrate practical engineering rather than a collection of isolated scripts.

It combines:

```text
Python
+
SQL
+
APIs
+
Data Engineering
+
Analytics
+
Statistics
+
Visualization
+
Testing
+
Git
+
CI/CD
+
Cloud Automation
```

The objective is to demonstrate how a real data workflow can move from **raw external data → validated data → analytical intelligence → automated delivery**.

---

## 📌 Project Status

**Current version:** `v0.1`

**Status:** 🟢 Automated pipeline operational

The pipeline currently runs through GitHub Actions and can execute independently of a local development machine.

---

## 👨‍💻 Author

**Shreysth Goyal**

Built as an end-to-end data engineering and analytics portfolio project.

---

⭐ If you find the project useful, consider giving the repository a star.
