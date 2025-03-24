import json
import os
from dataclasses import dataclass
from typing import Dict, Optional

import httpx


@dataclass
class MimecastConfig:
    base_url: str = "https://api.services.mimecast.com"
    auth_path: str = "/oauth/token"
    notifications_path: str = "/api/account/get-dashboard-notifications"
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

class MimecastAuthenticator:
    def __init__(self, config: MimecastConfig):
        self.config = config
        self.token: Optional[str] = None

    def get_token(self) -> str:
        """Obtain authentication token from Mimecast API."""
        if not self.token:
            auth_payload = (
                f"client_id={self.config.client_id}"
                f"&client_secret={self.config.client_secret}"
                f"&grant_type=client_credentials"
            )
            auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

            with httpx.Client() as client:
                response = client.post(
                    f"{self.config.base_url}{self.config.auth_path}",
                    headers=auth_headers,
                    data=auth_payload
                )
                self.token = response.json()["access_token"]
        return self.token

class MimecastClient:
    def __init__(self):
        self.config = MimecastConfig(
            client_id=os.getenv("MIME_ID"),
            client_secret=os.getenv("MIME_SECRET")
        )
        self.authenticator = MimecastAuthenticator(self.config)

    def get_notifications(self) -> Dict:
        """Fetch notifications from the Mimecast API."""
        token = self.authenticator.get_token()
        headers = {"Authorization": f"Bearer {token}"}

        with httpx.Client() as client:
            response = client.post(
                f"{self.config.base_url}{self.config.notifications_path}",
                headers=headers
            )
            return response.json()

    @staticmethod
    def save_notifications(data: Dict, filename: str = "dash_notifications_py.json") -> None:
        """Save notifications data to a JSON file."""
        with open(filename, "w", newline="\n") as f:
            json.dump(data, f, indent=2)

def main():
    client = MimecastClient()
    notifications = client.get_notifications()
    client.save_notifications(notifications)

if __name__ == "__main__":
    main()
