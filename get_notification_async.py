import asyncio
import json
import os

import aiohttp


async def get_notifications():
    base_url = "https://api.services.mimecast.com"
    auth_path = "/oauth/token"
    r_path = "/api/account/get-dashboard-notifications"
    client_id = os.getenv("MIME_ID")
    client_secret = os.getenv("MIME_SECRET")

    # Format auth payload as URL-encoded string
    auth_payload = f"client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with aiohttp.ClientSession() as session:
        # Get authentication token
        async with session.post(
            base_url + auth_path,
            headers=auth_headers,
            data=auth_payload  # Send as string, not dict
        ) as response:
            auth_data = await response.json()
            bearer_token = auth_data["access_token"]

        # Get notifications with correct headers
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        async with session.post(
            base_url + r_path,
            headers=headers,
            json={}
        ) as response:
            data = await response.json()

            # Save to file
            with open("dash_notifications.json", "w", newline="\n") as f:
                json.dump(data, f, indent=2)

            return data

async def main():
    await get_notifications()

if __name__ == "__main__":
    asyncio.run(main())
