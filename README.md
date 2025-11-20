# Peloton Analysis

Extract and analyze personal Peloton ride data to gain insights into performance, progress, and patterns.

## Overview

This project provides tools to:
- Extract ride data from Peloton's API
- Store and organize workout history
- Analyze performance metrics and trends
- Visualize progress over time

## Project Structure

```
peloton-analysis/
├── src/
│   ├── extraction/      # Data extraction from Peloton API
│   ├── analysis/        # Analysis scripts and notebooks
│   └── visualization/   # Visualization tools
├── data/                # Stored ride data (gitignored)
├── notebooks/           # Jupyter notebooks for exploration
└── docs/                # Documentation
```

## Setup

### 1. Clone and Install

```bash
git clone https://github.com/pqzdev/peloton-analysis.git
cd peloton-analysis

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Your Peloton Data

**Important:** As of November 2025, Peloton has blocked the unofficial API endpoint. Use the official CSV export instead:

1. Go to https://members.onepeloton.com/profile/workouts
2. Sign in with your Peloton credentials
3. Click **"DOWNLOAD WORKOUTS"** button (top right)
4. Save the CSV file to your computer

**Note:** This feature requires your language to be set to English and is only available via web browser.

### 3. Import Your Data

```bash
python scripts/import_csv.py ~/Downloads/workouts.csv
```

This will:
- Load your workout data from the CSV
- Convert to JSON format
- Save to `data/raw/workouts_latest.json`
- Display summary statistics

### Explore Your Data

Check the [notebooks/](notebooks/) directory for Jupyter notebooks to explore and analyze your data:

```bash
jupyter notebook
```

## Features

- **Authentication**: Secure session-based authentication with Peloton API
- **Data Extraction**: Fetch workout history, performance metrics, and ride details
- **Rate Limiting**: Built-in rate limiting to be respectful of API usage
- **Comprehensive Data**: Includes ride details, instructor info, and performance metrics

## Development Roadmap

See [PLAN.md](PLAN.md) for the complete development roadmap including:
- Phase 1: Data extraction (✓ In Progress)
- Phase 2: Data processing & enrichment
- Phase 3: Analysis & insights
- Phase 4: Visualization & reporting
- Phase 5: Advanced features

## License

MIT
