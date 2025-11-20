"""
Peloton API Client

Provides methods for interacting with the Peloton API endpoints.
"""

import requests
from typing import Dict, Any, List, Optional
import logging
import time

logger = logging.getLogger(__name__)


class PelotonAPIClient:
    """Client for making requests to the Peloton API."""

    BASE_URL = "https://api.onepeloton.com"

    def __init__(self, session: requests.Session, user_id: str):
        """
        Initialize the API client.

        Args:
            session: Authenticated requests.Session
            user_id: Peloton user ID
        """
        self.session = session
        self.user_id = user_id

        # Rate limiting
        self.min_request_interval = 0.1  # seconds between requests
        self.last_request_time = 0

    def _rate_limit(self) -> None:
        """Implement basic rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make an API request with rate limiting and error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers

        Returns:
            JSON response as dictionary

        Raises:
            requests.HTTPError: On HTTP errors
        """
        self._rate_limit()

        url = f"{self.BASE_URL}{endpoint}"
        default_headers = {"peloton-platform": "web"}

        if headers:
            default_headers.update(headers)

        try:
            response = self.session.request(
                method=method, url=url, params=params, headers=default_headers
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for {endpoint}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error making request to {endpoint}: {e}")
            raise

    def get_user_profile(self) -> Dict[str, Any]:
        """
        Get the current user's profile.

        Returns:
            User profile data
        """
        logger.info("Fetching user profile...")
        return self._make_request("GET", "/api/me")

    def get_user_overview(self) -> Dict[str, Any]:
        """
        Get user overview statistics.

        Returns:
            User overview data including stats
        """
        logger.info("Fetching user overview...")
        return self._make_request("GET", f"/api/user/{self.user_id}/overview")

    def get_workouts(
        self, page: int = 0, limit: int = 100, joins: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get user's workout history.

        Args:
            page: Page number (0-indexed)
            limit: Number of workouts per page (max 100)
            joins: Comma-separated list of related data to include
                   (e.g., "ride,ride.instructor")

        Returns:
            Workout data including list of workouts and pagination info
        """
        logger.info(f"Fetching workouts (page {page}, limit {limit})...")
        params = {"page": page, "limit": limit}
        if joins:
            params["joins"] = joins

        return self._make_request("GET", f"/api/user/{self.user_id}/workouts", params=params)

    def get_all_workouts(self, joins: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all user workouts by paginating through results.

        Args:
            joins: Comma-separated list of related data to include

        Returns:
            List of all workout data
        """
        logger.info("Fetching all workouts...")
        all_workouts = []
        page = 0
        limit = 100

        while True:
            response = self.get_workouts(page=page, limit=limit, joins=joins)
            workouts = response.get("data", [])

            if not workouts:
                break

            all_workouts.extend(workouts)
            logger.info(f"Fetched {len(all_workouts)} workouts so far...")

            # Check if there are more pages
            if len(workouts) < limit:
                break

            page += 1

        logger.info(f"Fetched total of {len(all_workouts)} workouts")
        return all_workouts

    def get_workout_detail(self, workout_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific workout.

        Args:
            workout_id: Workout ID

        Returns:
            Detailed workout data
        """
        logger.info(f"Fetching workout detail for {workout_id}...")
        return self._make_request("GET", f"/api/workout/{workout_id}")

    def get_workout_performance_graph(
        self, workout_id: str, every_n: int = 1
    ) -> Dict[str, Any]:
        """
        Get second-by-second performance data for a workout.

        Args:
            workout_id: Workout ID
            every_n: Sample every N seconds (default 1 for all data)

        Returns:
            Performance graph data with metrics
        """
        logger.info(f"Fetching performance graph for workout {workout_id}...")
        params = {"every_n": every_n}
        return self._make_request(
            "GET", f"/api/workout/{workout_id}/performance_graph", params=params
        )

    def get_ride_detail(self, ride_id: str) -> Dict[str, Any]:
        """
        Get information about a specific ride/class.

        Args:
            ride_id: Ride ID

        Returns:
            Ride/class data
        """
        logger.info(f"Fetching ride detail for {ride_id}...")
        return self._make_request("GET", f"/api/ride/{ride_id}/details")

    def get_instructor(self, instructor_id: str) -> Dict[str, Any]:
        """
        Get information about a specific instructor.

        Args:
            instructor_id: Instructor ID

        Returns:
            Instructor data
        """
        logger.info(f"Fetching instructor detail for {instructor_id}...")
        return self._make_request("GET", f"/api/instructor/{instructor_id}")
