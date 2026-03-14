import json
import os
import sys
from datetime import datetime, timezone

from app.integrations.telit_client import (
    TelitAuthenticationError,
    TelitClient,
    TelitSMSDeliveryError,
)


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    try:
        base_url = get_required_env("TELIT_API_BASE_URL")
        test_msisdn = get_required_env("TELIT_TEST_MSISDN")
        test_message = os.getenv("TELIT_TEST_MESSAGE", "!R0")

        print("=" * 80)
        print("TELIT SMS SMOKE TEST")
        print("=" * 80)
        print(f"Timestamp (UTC): {datetime.now(timezone.utc).isoformat()}")
        print(f"Base URL: {base_url}")
        print(f"Target MSISDN: {test_msisdn}")
        print(f"Message: {test_message}")
        print("-" * 80)

        client = TelitClient()
        result = client.send_sms(msisdn=test_msisdn, message=test_message)

        print("SMS Send Result:")
        print(json.dumps(result, indent=2))
        print("=" * 80)
        print("Smoke test completed successfully.")

    except (TelitAuthenticationError, TelitSMSDeliveryError, ValueError) as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"UNEXPECTED ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()