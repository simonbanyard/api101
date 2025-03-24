import json
import os

import requests

base_url = "https://api.services.mimecast.com"
auth_path = "/oauth/token"
r_path = "/api/account/get-dashboard-notifications"
client_id = os.getenv("MIME_ID")
client_secret = os.getenv("MIME_SECRET")

auth_payload = f"client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

r_auth = requests.request("POST", base_url + auth_path, headers=auth_headers, data=auth_payload)
bearer_token = r_auth.json()["access_token"]

payload = {}
headers = {"Authorization": f"Bearer {bearer_token}"}

r = requests.request("POST", base_url + r_path, headers=headers, data=payload)
response = r.json()
print(json.dumps(response, indent=2))


with open("dash_notifications.json", "w", newline="\n") as f:
    json.dump(response, f, indent=2)
