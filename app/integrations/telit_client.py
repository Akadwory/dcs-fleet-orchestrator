"""That file will hold:
authentication
SMS send logic
reusable request handling

three responsibilities for now:
authenticate with Telit
send SMS by msisdn
return a clean structured result"""
import os
from typing import Dict, Any
import requests


class TelitAuthenticationError(Exception):
    pass


class TelitSMSDeliveryError(Exception):
    pass


class TelitClient:
    """
    Telit API integration client.

    Handles:
    - authentication
    - SMS sending
    """

    def __init__(self) -> None:
        self.base_url = os.getenv("TELIT_API_BASE_URL")
        self.username = os.getenv("TELIT_API_USERNAME")
        self.password = os.getenv("TELIT_API_PASSWORD")

        if not self.base_url:
            raise ValueError("TELIT_API_BASE_URL not set")

        if not self.username:
            raise ValueError("TELIT_API_USERNAME not set")

        if not self.password:
            raise ValueError("TELIT_API_PASSWORD not set")

        self.session_id: str | None = None

    def authenticate(self) -> str:
        payload = {
            "auth": {
                "command": "api.authenticate",
                "params": {
                    "username": self.username,
                    "password": self.password,
                },
            }
        }

        response = requests.post(
            self.base_url,
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            raise TelitAuthenticationError(
                f"Telit auth HTTP error: {response.status_code}"
            )

        data = response.json()

        auth = data.get("auth", {})
        if not auth.get("success"):
            raise TelitAuthenticationError(
                f"Telit authentication failed: {data}"
            )

        session_id = auth["params"]["sessionId"]
        self.session_id = session_id

        return session_id

    def send_sms(self, msisdn: str, message: str) -> Dict[str, Any]:
        if not self.session_id:
            self.authenticate()

        payload = {
            "auth": {
                "sessionId": self.session_id
            },
            "1": {
                "command": "sms.send",
                "params": {
                    "msisdn": msisdn,
                    "message": message,
                    "coding": "SEVEN_BIT",
                },
            },
        }

        response = requests.post(
            self.base_url,
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            raise TelitSMSDeliveryError(
                f"Telit SMS HTTP error: {response.status_code}"
            )

        data = response.json()

        sms_result = data.get("1", {})
        if not sms_result.get("success"):
            raise TelitSMSDeliveryError(
                f"SMS send failed: {data}"
            )

        return sms_result["params"]

