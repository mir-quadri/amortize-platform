"""Smoke test for deployed service."""

import json
import time
from decimal import Decimal

import requests

MAX_RETRIES = 30
RETRY_DELAY = 2


def smoke_test() -> None:
    """Test that deployed service calculates amortization correctly."""
    url = "http://localhost:8000/v1/amortization"
    payload = {
        "principal": "300000",
        "annual_rate_pct": "6",
        "term_months": 360,
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            data = response.json()

            monthly_payment = Decimal(data["monthly_payment"])
            expected_payment = Decimal("1798.65")

            print(f"Response: {json.dumps(data, indent=2, default=str)}")

            with open("/tmp/smoke-test-response.json", "w") as f:
                json.dump(data, f, indent=2, default=str)

            if monthly_payment == expected_payment:
                print("\n✓ SMOKE TEST PASSED")
                print(f"  Expected: {expected_payment}")
                print(f"  Got:      {monthly_payment}")
                return

            print("\n✗ SMOKE TEST FAILED")
            print(f"  Expected monthly payment: {expected_payment}")
            print(f"  Got:                     {monthly_payment}")
            raise AssertionError(
                f"Monthly payment mismatch: expected {expected_payment}, got {monthly_payment}"
            )

        except (requests.ConnectionError, requests.Timeout):
            if attempt < MAX_RETRIES - 1:
                print(
                    f"Attempt {attempt + 1}/{MAX_RETRIES}: Connection failed, retrying in {RETRY_DELAY}s..."
                )
                time.sleep(RETRY_DELAY)
            else:
                print(f"✗ Failed to connect after {MAX_RETRIES} attempts")
                raise


if __name__ == "__main__":
    smoke_test()
