"""Integration tests for app and calculator."""

from decimal import Decimal

from fastapi.testclient import TestClient

from src.amortize.app import app
from src.amortize.calculator import calculate_amortization

client = TestClient(app)


class TestCalculatorIntegration:
    """Tests for calculator edge cases and integrations."""

    def test_boundary_min_principal(self) -> None:
        """Test minimum principal (just above 0)."""
        principal = Decimal("0.01")
        annual_rate = Decimal("0")
        months = 1

        result = calculate_amortization(principal, annual_rate, months)

        assert result["monthly_payment"] == Decimal("0.01")
        assert result["total_interest"] == Decimal("0")

    def test_boundary_max_rate(self) -> None:
        """Test maximum interest rate (50%)."""
        principal = Decimal("1000")
        annual_rate = Decimal("50")
        months = 12

        result = calculate_amortization(principal, annual_rate, months)

        assert result["monthly_payment"] > Decimal("0")
        assert len(result["schedule"]) == 12

    def test_boundary_max_term(self) -> None:
        """Test maximum term (480 months = 40 years)."""
        principal = Decimal("100000")
        annual_rate = Decimal("5")
        months = 480

        result = calculate_amortization(principal, annual_rate, months)

        assert len(result["schedule"]) == 480
        assert result["schedule"][-1]["balance"] <= Decimal("0.01")

    def test_mid_range_values(self) -> None:
        """Test typical mid-range loan."""
        principal = Decimal("150000")
        annual_rate = Decimal("4.5")
        months = 180

        result = calculate_amortization(principal, annual_rate, months)

        assert len(result["schedule"]) == 180
        first = result["schedule"][0]
        last = result["schedule"][-1]

        assert first["interest"] > last["interest"]
        assert first["principal"] < last["principal"]


class TestAPIEdgeCases:
    """Test API edge cases."""

    def test_max_term_via_api(self) -> None:
        """Test maximum term through API."""
        payload = {
            "principal": "10000",
            "annual_rate_pct": "5",
            "term_months": 480,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        assert len(response.json()["schedule"]) == 480

    def test_min_term_via_api(self) -> None:
        """Test minimum term through API."""
        payload = {
            "principal": "1000",
            "annual_rate_pct": "5",
            "term_months": 1,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        assert len(response.json()["schedule"]) == 1

    def test_float_decimal_conversion(self) -> None:
        """Test that float inputs are properly converted to Decimal."""
        payload = {
            "principal": 50000.5,
            "annual_rate_pct": 4.75,
            "term_months": 60,
        }
        response = client.post("/v1/amortization", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "monthly_payment" in data
