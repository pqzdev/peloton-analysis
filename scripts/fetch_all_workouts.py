#!/usr/bin/env python3
"""
Fetch all workout data from Peloton and save to JSON.

Usage:
    python scripts/fetch_all_workouts.py
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extraction.peloton import PelotonClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Fetch all workouts and save to JSON."""
    logger.info("=" * 60)
    logger.info("Fetching All Peloton Workout Data")
    logger.info("=" * 60)

    try:
        # Create data directory if it doesn't exist
        data_dir = Path(__file__).parent.parent / "data" / "raw"
        data_dir.mkdir(parents=True, exist_ok=True)

        # Create client and connect
        logger.info("\nConnecting to Peloton API...")
        client = PelotonClient()

        if not client.connect():
            logger.error("Failed to connect. Check your credentials.")
            return 1

        # Fetch all workouts with related data
        logger.info("\nFetching all workouts (this may take a while)...")
        logger.info("Including ride and instructor data...")

        workouts = client.get_all_workouts(joins="ride,ride.instructor")

        logger.info(f"\n✓ Successfully fetched {len(workouts)} workouts")

        # Save to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = data_dir / f"workouts_{timestamp}.json"

        logger.info(f"\nSaving to {output_file}...")

        with open(output_file, 'w') as f:
            json.dump(workouts, f, indent=2)

        logger.info(f"✓ Saved {len(workouts)} workouts to {output_file}")

        # Also save the latest version
        latest_file = data_dir / "workouts_latest.json"
        with open(latest_file, 'w') as f:
            json.dump(workouts, f, indent=2)

        logger.info(f"✓ Also saved to {latest_file}")

        # Print summary statistics
        logger.info("\n" + "=" * 60)
        logger.info("Summary Statistics")
        logger.info("=" * 60)

        # Count by fitness discipline
        disciplines = {}
        for workout in workouts:
            ride = workout.get('ride', {})
            discipline = ride.get('fitness_discipline', 'Unknown')
            disciplines[discipline] = disciplines.get(discipline, 0) + 1

        logger.info("\nWorkouts by Type:")
        for discipline, count in sorted(disciplines.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {discipline}: {count}")

        # Calculate total output
        total_output = sum(
            workout.get('total_work', 0) / 1000
            for workout in workouts
            if workout.get('total_work')
        )
        logger.info(f"\nTotal Output Across All Workouts: {total_output:.1f} kJ")

        # Disconnect
        client.disconnect()

        logger.info("\n" + "=" * 60)
        logger.info("✓ Data fetch complete!")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"\n✗ Error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
