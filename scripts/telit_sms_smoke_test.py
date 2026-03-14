import json
import os
import sys
from datetime import datetime, timezone

import requests


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def build_payload(msisdn: str, message: str) -> dict:
    return {
        "auth": {
            "command": "api.authenticate",
            "params": {
                "username": get_required_env("TELIT_API_USERNAME"),
                "password": get_required_env("TELIT_API_PASSWORD"),
            },
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


def main() -> None:
    try:
        base_url = get_required_env("TELIT_API_BASE_URL")
        username = get_required_env("TELIT_API_USERNAME")
        password = get_required_env("TELIT_API_PASSWORD")
        test_msisdn = get_required_env("TELIT_TEST_MSISDN")
        test_message = os.getenv("TELIT_TEST_MESSAGE", "!R0")

        auth_payload = {
            "auth": {
                "command": "api.authenticate",
                "params": {
                    "username": username,
                    "password": password,
                },
            }
        }

        print("=" * 80)
        print("TELIT SMS SMOKE TEST")
        print("=" * 80)
        print(f"Timestamp (UTC): {datetime.now(timezone.utc).isoformat()}")
        print(f"Base URL: {base_url}")
        print(f"Target MSISDN: {test_msisdn}")
        print(f"Message: {test_message}")
        print("-" * 80)
        print("STEP 1: AUTHENTICATE")
        safe_auth_payload = json.loads(json.dumps(auth_payload))
        safe_auth_payload["auth"]["params"]["password"] = "********"
        print(json.dumps(safe_auth_payload, indent=2))

        auth_response = requests.post(
            base_url,
            json=auth_payload,
            timeout=30,
            headers={"Content-Type": "application/json"},
        )

        print(f"Auth HTTP Status Code: {auth_response.status_code}")
        auth_json = auth_response.json()
        print("Auth Response Body:")
        print(json.dumps(auth_json, indent=2))

        if auth_response.status_code != 200:
            sys.exit(1)

        auth_result = auth_json.get("auth", {})
        if not auth_result.get("success", False):
            sys.exit(1)

        session_id = auth_result["params"]["sessionId"]

        sms_payload = {
            "auth": {
                "sessionId": session_id
            },
            "1": {
                "command": "sms.send",
                "params": {
                    "msisdn": test_msisdn,
                    "message": test_message,
                    "coding": "SEVEN_BIT",
                },
            },
        }

        print("-" * 80)
        print("STEP 2: SEND SMS")
        print(json.dumps({
            "auth": {"sessionId": "********"},
            "1": sms_payload["1"]
        }, indent=2))

        sms_response = requests.post(
            base_url,
            json=sms_payload,
            timeout=30,
            headers={"Content-Type": "application/json"},
        )

        print(f"SMS HTTP Status Code: {sms_response.status_code}")
        sms_json = sms_response.json()
        print("SMS Response Body:")
        print(json.dumps(sms_json, indent=2))
        print("=" * 80)

        if sms_response.status_code != 200:
            sys.exit(1)

        sms_result = sms_json.get("1", {})
        if not sms_result.get("success", False):
            sys.exit(1)

        print("Smoke test completed successfully.")

    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()