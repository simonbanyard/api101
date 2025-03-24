import json
import os
from typing import Dict

import httpx


def get_config() -> Dict[str, str]:
    """Return configuration settings for the API."""
    return {
        "base_url": "https://api.services.mimecast.com",
        "auth_path": "/oauth/token",
        "notifications_path": "/api/account/get-dashboard-notifications",
        "client_id": os.getenv("MIME_ID"),
        "client_secret": os.getenv("MIME_SECRET")
    }

def get_auth_token(config: Dict[str, str]) -> str:
    """Obtain authentication token from Mimecast API."""
    auth_payload = (
        f"client_id={config['client_id']}"
        f"&client_secret={config['client_secret']}"
        f"&grant_type=client_credentials"
    )
    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = httpx.post(
        config["base_url"] + config["auth_path"],
        headers=auth_headers,
        data=auth_payload
    )
    return response.json()["access_token"]

def get_notifications(config: Dict[str, str], token: str) -> Dict:
    """Fetch notifications from the Mimecast API."""
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.post(
        config["base_url"] + config["notifications_path"],
        headers=headers
    )
    return response.json()

def save_to_file(data: Dict, filename: str) -> None:
    """Save JSON data to a file."""
    with open(filename, "w", newline="\n") as f:
        json.dump(data, f, indent=2)

def main() -> None:
    """Main execution flow."""
    config = get_config()
    token = get_auth_token(config)
    notifications = get_notifications(config, token)
    save_to_file(notifications, "dash_notifications_py.json")

if __name__ == "__main__":
    main()
