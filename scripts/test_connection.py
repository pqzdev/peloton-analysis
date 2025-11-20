#!/usr/bin/env python3
"""
Test script to verify Peloton API connection and basic data retrieval.

Usage:
    python scripts/test_connection.py
"""

import sys
import logging
from pathlib import Path

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
    """Test Peloton API connection."""
    logger.info("=" * 60)
    logger.info("Peloton API Connection Test")
    logger.info("=" * 60)

    try:
        # Create client (will load credentials from .env)
        logger.info("\n1. Creating Peloton client...")
        client = PelotonClient()

        # Connect
        logger.info("\n2. Connecting to Peloton API...")
        if not client.connect():
            logger.error("Failed to connect. Check your credentials in .env")
            return 1

        # Get profile
        logger.info("\n3. Fetching user profile...")
        profile = client.get_profile()
        logger.info(f"   Username: {profile.get('username')}")
        logger.info(f"   User ID: {profile.get('id')}")
        logger.info(f"   Location: {profile.get('location')}")

        # Get overview
        logger.info("\n4. Fetching user overview/stats...")
        overview = client.get_overview()
        logger.info(f"   Total workouts: {overview.get('workout_counts', [{}])[0].get('count', 'N/A')}")

        # Get recent workouts
        logger.info("\n5. Fetching recent workouts (last 5)...")
        workouts_response = client.get_workouts(page=0, limit=5, joins="ride,ride.instructor")
        workouts = workouts_response.get('data', [])

        logger.info(f"   Found {len(workouts)} recent workouts:")
        for i, workout in enumerate(workouts, 1):
            ride = workout.get('ride', {})
            instructor = ride.get('instructor', {})

            logger.info(f"\n   Workout {i}:")
            logger.info(f"      ID: {workout.get('id')}")
            logger.info(f"      Date: {workout.get('created_at')}")
            logger.info(f"      Class: {ride.get('title', 'N/A')}")
            logger.info(f"      Instructor: {instructor.get('name', 'N/A')}")
            logger.info(f"      Duration: {ride.get('duration', 0) / 60:.0f} minutes")

            # Try to get basic metrics
            total_work = workout.get('total_work')
            if total_work:
                logger.info(f"      Total Output: {total_work / 1000:.1f} kJ")

        # Disconnect
        logger.info("\n6. Disconnecting...")
        client.disconnect()

        logger.info("\n" + "=" * 60)
        logger.info("✓ All tests passed! API connection working.")
        logger.info("=" * 60)
        return 0

    except ValueError as e:
        logger.error(f"\n✗ Configuration error: {e}")
        logger.error("Make sure to create a .env file with your credentials.")
        logger.error("See .env.example for the template.")
        return 1

    except Exception as e:
        logger.error(f"\n✗ Error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
