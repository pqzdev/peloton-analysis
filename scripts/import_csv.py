#!/usr/bin/env python3
"""
Import Peloton workout data from CSV export.

Download your CSV from: https://members.onepeloton.com/profile/workouts
Then run: python scripts/import_csv.py path/to/your/workouts.csv

Usage:
    python scripts/import_csv.py ~/Downloads/workouts.csv
"""

import sys
import json
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def import_csv(csv_path: str) -> pd.DataFrame:
    """
    Import Peloton workout CSV and convert to structured format.

    Args:
        csv_path: Path to the Peloton workouts CSV file

    Returns:
        DataFrame with processed workout data
    """
    logger.info(f"Loading CSV from {csv_path}...")

    try:
        df = pd.read_csv(csv_path)
        logger.info(f"✓ Loaded {len(df)} workouts from CSV")

        # Display column names to help with processing
        logger.info(f"Columns found: {', '.join(df.columns.tolist())}")

        return df

    except FileNotFoundError:
        logger.error(f"File not found: {csv_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        raise


def save_processed_data(df: pd.DataFrame, output_dir: Path):
    """
    Save processed data to JSON format.

    Args:
        df: DataFrame with workout data
        output_dir: Directory to save output files
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save as JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = output_dir / f"workouts_csv_import_{timestamp}.json"

    logger.info(f"Saving to {json_file}...")
    df.to_json(json_file, orient='records', indent=2, date_format='iso')

    # Also save as latest
    latest_file = output_dir / "workouts_latest.json"
    df.to_json(latest_file, orient='records', indent=2, date_format='iso')

    logger.info(f"✓ Saved {len(df)} workouts to {json_file}")
    logger.info(f"✓ Also saved to {latest_file}")


def print_summary(df: pd.DataFrame):
    """Print summary statistics."""
    logger.info("\n" + "=" * 60)
    logger.info("WORKOUT SUMMARY")
    logger.info("=" * 60)

    logger.info(f"\nTotal Workouts: {len(df)}")

    # Check for common column names (these may vary)
    possible_type_cols = ['Fitness Discipline', 'Workout Type', 'Type']
    type_col = None
    for col in possible_type_cols:
        if col in df.columns:
            type_col = col
            break

    if type_col:
        logger.info(f"\nWorkouts by {type_col}:")
        counts = df[type_col].value_counts()
        for workout_type, count in counts.items():
            logger.info(f"  {workout_type}: {count}")

    # Look for date columns
    possible_date_cols = ['Workout Timestamp', 'Date', 'Created At']
    date_col = None
    for col in possible_date_cols:
        if col in df.columns:
            date_col = col
            break

    if date_col:
        try:
            dates = pd.to_datetime(df[date_col])
            logger.info(f"\nDate Range: {dates.min()} to {dates.max()}")
        except:
            pass

    logger.info("\n" + "=" * 60)


def main():
    """Main import function."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_csv.py path/to/workouts.csv")
        print("\nDownload your CSV from:")
        print("https://members.onepeloton.com/profile/workouts")
        print("(Click 'DOWNLOAD WORKOUTS' button)")
        return 1

    csv_path = sys.argv[1]

    logger.info("=" * 60)
    logger.info("Peloton CSV Import")
    logger.info("=" * 60)

    try:
        # Import CSV
        df = import_csv(csv_path)

        # Print summary
        print_summary(df)

        # Save processed data
        data_dir = Path(__file__).parent.parent / "data" / "raw"
        save_processed_data(df, data_dir)

        logger.info("\n✓ Import complete!")
        logger.info("\nNext steps:")
        logger.info("1. Explore your data with: jupyter notebook")
        logger.info("2. Open: notebooks/01_initial_exploration.ipynb")

        return 0

    except Exception as e:
        logger.error(f"\n✗ Error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
