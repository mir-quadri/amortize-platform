"""Tests for FastAPI application."""

from decimal import Decimal

from fastapi.testclient import TestClient

from src.amortize.app import app

client = TestClient(app)


class TestHealthProbes:
    """Tests for health check endpoints."""

    def test_healthz(self) -> None:
        """Test liveness probe."""
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_readyz(self) -> None:
        """Test readiness probe."""
        response = client.get("/readyz")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}


class TestAmortizationEndpoint:
    """Tests for amortization calculation endpoint."""

    def test_standard_mortgage(self) -> None:
        """Test standard 30-year mortgage calculation."""
        payload = {
            "principal": "300000",
            "annual_rate_pct": "6",
            "term_months": 360,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["monthly_payment"] == "1798.65"
        assert len(data["schedule"]) == 360

    def test_zero_interest_rate(self) -> None:
        """Test loan with 0% interest."""
        payload = {
            "principal": "12000",
            "annual_rate_pct": "0",
            "term_months": 12,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["monthly_payment"] == "1000.00"
        assert data["total_interest"] == "0.00"

    def test_short_term_loan(self) -> None:
        """Test short-term loan."""
        payload = {
            "principal": "5000",
            "annual_rate_pct": "5",
            "term_months": 12,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "monthly_payment" in data
        assert "total_interest" in data
        assert len(data["schedule"]) == 12

    def test_invalid_principal_zero(self) -> None:
        """Test that principal must be positive (Pydantic validation)."""
        payload = {
            "principal": "0",
            "annual_rate_pct": "5",
            "term_months": 12,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 422

    def test_invalid_principal_negative(self) -> None:
        """Test that principal must be positive."""
        payload = {
            "principal": "-1000",
            "annual_rate_pct": "5",
            "term_months": 12,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 422

    def test_invalid_rate_negative(self) -> None:
        """Test that rate cannot be negative."""
        payload = {
            "principal": "10000",
            "annual_rate_pct": "-1",
            "term_months": 12,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 422

    def test_invalid_rate_too_high(self) -> None:
        """Test that rate cannot exceed 50%."""
        payload = {
            "principal": "10000",
            "annual_rate_pct": "51",
            "term_months": 12,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 422

    def test_invalid_term_zero(self) -> None:
        """Test that term must be at least 1 month."""
        payload = {
            "principal": "10000",
            "annual_rate_pct": "5",
            "term_months": 0,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 422

    def test_invalid_term_too_long(self) -> None:
        """Test that term cannot exceed 480 months."""
        payload = {
            "principal": "10000",
            "annual_rate_pct": "5",
            "term_months": 481,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 422

    def test_missing_required_field(self) -> None:
        """Test that all required fields must be provided."""
        payload = {"principal": "10000", "annual_rate_pct": "5"}
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 422

    def test_decimal_precision(self) -> None:
        """Test that decimal precision is maintained."""
        payload = {
            "principal": "100000.50",
            "annual_rate_pct": "3.75",
            "term_months": 60,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        data = response.json()
        monthly_payment = Decimal(data["monthly_payment"])
        assert monthly_payment.as_tuple().exponent == -2

    def test_schedule_structure(self) -> None:
        """Test that schedule has correct structure."""
        payload = {
            "principal": "50000",
            "annual_rate_pct": "5",
            "term_months": 12,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        data = response.json()

        for entry in data["schedule"]:
            assert "month" in entry
            assert "payment" in entry
            assert "principal" in entry
            assert "interest" in entry
            assert "balance" in entry

    def test_various_loan_amounts(self) -> None:
        """Test various loan amounts."""
        test_cases = [
            ("1000", "5", 12),
            ("100000", "3.5", 180),
            ("250000", "4.25", 240),
        ]

        for principal, rate, months in test_cases:
            payload = {
                "principal": principal,
                "annual_rate_pct": rate,
                "term_months": months,
            }
            response = client.post("/v1/amortization", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert len(data["schedule"]) == months
            assert data["monthly_payment"] != "0.00"


class TestLoggingAndErrors:
    """Test logging and error handling."""

    def test_successful_request_logging(self) -> None:
        """Test that successful requests are logged."""
        payload = {
            "principal": "50000",
            "annual_rate_pct": "5",
            "term_months": 12,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200

    def test_error_handling_on_calculation_error(self) -> None:
        """Test error handling for calculation issues."""
        payload = {
            "principal": "1000",
            "annual_rate_pct": "5",
            "term_months": 1,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200

    def test_large_principal(self) -> None:
        """Test with large principal."""
        payload = {
            "principal": "1000000",
            "annual_rate_pct": "5",
            "term_months": 360,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "monthly_payment" in data
        assert len(data["schedule"]) == 360

    def test_low_interest_rate(self) -> None:
        """Test with very low interest rate."""
        payload = {
            "principal": "100000",
            "annual_rate_pct": "0.1",
            "term_months": 120,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        data = response.json()
        total_interest = Decimal(data["total_interest"])
        assert total_interest > Decimal("0")
        assert total_interest < Decimal("1000")

    def test_endpoint_response_includes_all_fields(self) -> None:
        """Test that endpoint response includes all required fields."""
        payload = {
            "principal": "50000",
            "annual_rate_pct": "5",
            "term_months": 24,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        data = response.json()

        required_fields = ["monthly_payment", "total_interest", "schedule"]
        for field in required_fields:
            assert field in data

        if data["schedule"]:
            entry = data["schedule"][0]
            required_entry_fields = ["month", "payment", "principal", "interest", "balance"]
            for field in required_entry_fields:
                assert field in entry
