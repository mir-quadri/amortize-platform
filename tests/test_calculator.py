"""Tests for amortization calculator."""

from decimal import Decimal

import pytest

from src.amortize.calculator import calculate_amortization, calculate_monthly_payment


class TestMonthlyPayment:
    """Tests for monthly payment calculation."""

    def test_standard_mortgage(self) -> None:
        """Test standard 30-year mortgage: $300k principal, 6% APR, 360 months."""
        principal = Decimal("300000")
        annual_rate = Decimal("6")
        months = 360

        payment = calculate_monthly_payment(principal, annual_rate, months)

        assert payment == Decimal("1798.65")

    def test_zero_interest_rate(self) -> None:
        """Test loan with 0% interest."""
        principal = Decimal("12000")
        annual_rate = Decimal("0")
        months = 12

        payment = calculate_monthly_payment(principal, annual_rate, months)

        assert payment == Decimal("1000.00")

    def test_one_month_term(self) -> None:
        """Test one-month loan."""
        principal = Decimal("1000")
        annual_rate = Decimal("12")
        months = 1

        payment = calculate_monthly_payment(principal, annual_rate, months)

        assert payment == Decimal("1010.00")

    def test_high_interest_rate(self) -> None:
        """Test edge case with maximum interest rate."""
        principal = Decimal("10000")
        annual_rate = Decimal("50")
        months = 12

        payment = calculate_monthly_payment(principal, annual_rate, months)

        assert payment > Decimal("900")
        assert payment < Decimal("1100")

    def test_invalid_principal(self) -> None:
        """Test that principal must be positive."""
        with pytest.raises(ValueError, match="principal must be > 0"):
            calculate_monthly_payment(Decimal("0"), Decimal("5"), 12)

        with pytest.raises(ValueError, match="principal must be > 0"):
            calculate_monthly_payment(Decimal("-1000"), Decimal("5"), 12)

    def test_invalid_rate(self) -> None:
        """Test that rate must be within bounds."""
        with pytest.raises(ValueError, match="annual_rate_pct must be between 0 and 50"):
            calculate_monthly_payment(Decimal("10000"), Decimal("-1"), 12)

        with pytest.raises(ValueError, match="annual_rate_pct must be between 0 and 50"):
            calculate_monthly_payment(Decimal("10000"), Decimal("51"), 12)

    def test_invalid_term(self) -> None:
        """Test that term must be within bounds."""
        with pytest.raises(ValueError, match="term_months must be between 1 and 480"):
            calculate_monthly_payment(Decimal("10000"), Decimal("5"), 0)

        with pytest.raises(ValueError, match="term_months must be between 1 and 480"):
            calculate_monthly_payment(Decimal("10000"), Decimal("5"), 481)

    def test_small_principal(self) -> None:
        """Test very small principal."""
        principal = Decimal("1.00")
        annual_rate = Decimal("5")
        months = 12

        payment = calculate_monthly_payment(principal, annual_rate, months)

        assert payment > Decimal("0")
        assert payment <= Decimal("0.10")


class TestAmortizationSchedule:
    """Tests for full amortization schedule."""

    def test_standard_mortgage_schedule(self) -> None:
        """Test standard 30-year mortgage schedule."""
        principal = Decimal("300000")
        annual_rate = Decimal("6")
        months = 360

        result = calculate_amortization(principal, annual_rate, months)

        assert result["monthly_payment"] == Decimal("1798.65")
        assert len(result["schedule"]) == 360
        assert result["schedule"][0]["month"] == 1
        assert result["schedule"][-1]["month"] == 360

        first = result["schedule"][0]
        assert first["payment"] == Decimal("1798.65")
        assert first["principal"] > 0
        assert first["interest"] > 0
        assert first["balance"] < principal

        last = result["schedule"][-1]
        assert last["balance"] <= Decimal("0.01")

    def test_schedule_principal_sums_to_loan(self) -> None:
        """Test that principal payments sum to original loan (within rounding)."""
        principal = Decimal("50000")
        annual_rate = Decimal("7")
        months = 60

        result = calculate_amortization(principal, annual_rate, months)

        total_principal = sum(entry["principal"] for entry in result["schedule"])
        assert abs(total_principal - principal) < Decimal("0.01")

    def test_schedule_payment_equals_principal_plus_interest(self) -> None:
        """Test that each payment equals principal + interest."""
        principal = Decimal("100000")
        annual_rate = Decimal("5")
        months = 120

        result = calculate_amortization(principal, annual_rate, months)

        for entry in result["schedule"]:
            assert entry["payment"] == entry["principal"] + entry["interest"]

    def test_zero_interest_schedule(self) -> None:
        """Test schedule with 0% interest."""
        principal = Decimal("12000")
        annual_rate = Decimal("0")
        months = 12

        result = calculate_amortization(principal, annual_rate, months)

        assert result["total_interest"] == Decimal("0")
        assert result["monthly_payment"] == Decimal("1000.00")

        for entry in result["schedule"]:
            assert entry["interest"] == Decimal("0")
            assert entry["principal"] == Decimal("1000.00")

    def test_short_term_loan(self) -> None:
        """Test short-term loan (1 month)."""
        principal = Decimal("5000")
        annual_rate = Decimal("12")
        months = 1

        result = calculate_amortization(principal, annual_rate, months)

        assert len(result["schedule"]) == 1
        entry = result["schedule"][0]
        assert entry["month"] == 1
        assert entry["balance"] == Decimal("0")

    def test_balance_decreases_monotonically(self) -> None:
        """Test that remaining balance decreases each month."""
        principal = Decimal("25000")
        annual_rate = Decimal("4.5")
        months = 60

        result = calculate_amortization(principal, annual_rate, months)

        prev_balance = principal
        for entry in result["schedule"]:
            assert entry["balance"] < prev_balance or (
                entry["balance"] == Decimal("0") and prev_balance < Decimal("0.01")
            )
            prev_balance = entry["balance"]
