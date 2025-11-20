"""
Peloton API Authentication Module

Handles authentication with the Peloton API and session management.
"""

import requests
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PelotonAuthenticator:
    """Handles authentication with the Peloton API."""

    BASE_URL = "https://api.onepeloton.com"
    AUTH_ENDPOINT = f"{BASE_URL}/auth/login"

    def __init__(self, username: str, password: str):
        """
        Initialize the authenticator.

        Args:
            username: Peloton username or email
            password: Peloton password
        """
        self.username = username
        self.password = password
        self.session: Optional[requests.Session] = None
        self.user_id: Optional[str] = None
        self._authenticated = False

    def login(self) -> bool:
        """
        Authenticate with the Peloton API.

        Returns:
            True if authentication successful, False otherwise
        """
        try:
            self.session = requests.Session()

            payload = {
                'username_or_email': self.username,
                'password': self.password
            }

            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'peloton-analysis/0.1.0'
            }

            logger.info("Attempting to authenticate with Peloton API...")
            response = self.session.post(self.AUTH_ENDPOINT, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            self.user_id = data.get('user_id')

            if self.user_id:
                self._authenticated = True
                logger.info(f"Successfully authenticated. User ID: {self.user_id}")
                return True
            else:
                logger.error("Authentication response missing user_id")
                return False

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error during authentication: {e}")
            if e.response.status_code == 401:
                logger.error("Invalid credentials")
            return False
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            return False

    def is_authenticated(self) -> bool:
        """Check if currently authenticated."""
        return self._authenticated and self.session is not None

    def get_session(self) -> requests.Session:
        """
        Get the authenticated session.

        Returns:
            requests.Session object

        Raises:
            RuntimeError: If not authenticated
        """
        if not self.is_authenticated():
            raise RuntimeError("Not authenticated. Call login() first.")
        return self.session

    def get_user_id(self) -> str:
        """
        Get the authenticated user's ID.

        Returns:
            User ID string

        Raises:
            RuntimeError: If not authenticated
        """
        if not self.is_authenticated():
            raise RuntimeError("Not authenticated. Call login() first.")
        return self.user_id

    def logout(self) -> None:
        """Clear the session and authentication state."""
        if self.session:
            self.session.close()
            self.session = None
        self._authenticated = False
        self.user_id = None
        logger.info("Logged out successfully")
