import os
import requests
import base64
import datetime
import logging

logging.basicConfig(filename='data/log.txt')

FILENAME = f"data/{datetime.date.today()}.jpg"

IP_ADDR = os.environ.get("IP_ADDRESS")
PORT = os.environ.get("PORT", "8080")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")

SIGNAL_API_URL = f"http://{IP_ADDR}:{PORT}/v1"
url = f"{SIGNAL_API_URL}/profiles/{PHONE_NUMBER}"
headers = {
    "Content-Type": "application/json",
    "accept": "application/json",
}
if not os.path.exists(FILENAME):
    logging.error(f"{FILENAME} doesn't exist!")
    exit(1)

encoded_string = ""
with open(FILENAME, "rb") as f:
    encoded_string = base64.b64encode(f.read())

data = {
    "base64_avatar": encoded_string.decode('utf-8'),
    "name": "Houssem"
}
req_res = requests.put(url, headers=headers, json=data)
if req_res.status_code != 204:
    logging.error(f'Error making PUT request: {req_res.reason}')
    exit(1)

logging.info("Profile has been updated")
