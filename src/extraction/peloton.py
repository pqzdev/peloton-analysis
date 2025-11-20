"""
Peloton Client

High-level wrapper that combines authentication and API access.
"""

from typing import Optional, Dict, Any, List
import logging
from dotenv import load_dotenv
import os

from src.auth.authenticator import PelotonAuthenticator
from src.extraction.api_client import PelotonAPIClient

logger = logging.getLogger(__name__)


class PelotonClient:
    """High-level client for accessing Peloton data."""

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the Peloton client.

        Args:
            username: Peloton username/email (or set PELOTON_USERNAME env var)
            password: Peloton password (or set PELOTON_PASSWORD env var)
        """
        # Load environment variables
        load_dotenv()

        self.username = username or os.getenv("PELOTON_USERNAME")
        self.password = password or os.getenv("PELOTON_PASSWORD")

        if not self.username or not self.password:
            raise ValueError(
                "Username and password required. Provide as arguments or set "
                "PELOTON_USERNAME and PELOTON_PASSWORD environment variables."
            )

        self.authenticator = PelotonAuthenticator(self.username, self.password)
        self.api_client: Optional[PelotonAPIClient] = None

    def connect(self) -> bool:
        """
        Connect to Peloton API (authenticate).

        Returns:
            True if successful, False otherwise
        """
        if self.authenticator.login():
            session = self.authenticator.get_session()
            user_id = self.authenticator.get_user_id()
            self.api_client = PelotonAPIClient(session, user_id)
            logger.info("Successfully connected to Peloton API")
            return True
        return False

    def disconnect(self) -> None:
        """Disconnect from Peloton API."""
        self.authenticator.logout()
        self.api_client = None

    def _ensure_connected(self) -> None:
        """Ensure client is connected."""
        if self.api_client is None:
            raise RuntimeError("Not connected. Call connect() first.")

    @property
    def user_id(self) -> str:
        """Get the authenticated user's ID."""
        return self.authenticator.get_user_id()

    # Convenience methods that delegate to API client

    def get_profile(self) -> Dict[str, Any]:
        """Get user profile."""
        self._ensure_connected()
        return self.api_client.get_user_profile()

    def get_overview(self) -> Dict[str, Any]:
        """Get user overview with statistics."""
        self._ensure_connected()
        return self.api_client.get_user_overview()

    def get_workouts(
        self, page: int = 0, limit: int = 100, joins: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get paginated workout history."""
        self._ensure_connected()
        return self.api_client.get_workouts(page=page, limit=limit, joins=joins)

    def get_all_workouts(self, joins: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all workouts (handles pagination automatically)."""
        self._ensure_connected()
        return self.api_client.get_all_workouts(joins=joins)

    def get_workout_detail(self, workout_id: str) -> Dict[str, Any]:
        """Get detailed workout information."""
        self._ensure_connected()
        return self.api_client.get_workout_detail(workout_id)

    def get_workout_performance(
        self, workout_id: str, every_n: int = 1
    ) -> Dict[str, Any]:
        """Get second-by-second performance data."""
        self._ensure_connected()
        return self.api_client.get_workout_performance_graph(workout_id, every_n)

    def get_ride_detail(self, ride_id: str) -> Dict[str, Any]:
        """Get ride/class information."""
        self._ensure_connected()
        return self.api_client.get_ride_detail(ride_id)

    def get_instructor(self, instructor_id: str) -> Dict[str, Any]:
        """Get instructor information."""
        self._ensure_connected()
        return self.api_client.get_instructor(instructor_id)

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
