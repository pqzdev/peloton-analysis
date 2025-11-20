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

### 2. Configure Credentials

Create a `.env` file with your Peloton credentials:

```bash
cp .env.example .env
# Edit .env and add your credentials
```

Your `.env` should contain:
```
PELOTON_USERNAME=your_username_or_email
PELOTON_PASSWORD=your_password
```

### 3. Test Connection

```bash
python scripts/test_connection.py
```

This will authenticate and fetch your recent workout data to verify everything is working.

## Usage

### Fetch All Your Workout Data

```bash
python scripts/fetch_all_workouts.py
```

This will:
- Authenticate with Peloton
- Fetch all your workout history (with pagination)
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
