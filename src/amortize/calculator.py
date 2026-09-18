"""Amortization calculation logic."""

from decimal import ROUND_HALF_UP, Decimal
from typing import TypedDict


class AmortizationScheduleEntry(TypedDict):
    month: int
    payment: Decimal
    principal: Decimal
    interest: Decimal
    balance: Decimal


class AmortizationResult(TypedDict):
    monthly_payment: Decimal
    total_interest: Decimal
    schedule: list[AmortizationScheduleEntry]


def calculate_monthly_payment(
    principal: Decimal, annual_rate_pct: Decimal, term_months: int
) -> Decimal:
    """Calculate monthly payment using standard loan amortization formula.

    Args:
        principal: Loan amount in dollars
        annual_rate_pct: Annual interest rate as percentage (e.g., 6.0 for 6%)
        term_months: Number of months for the loan

    Returns:
        Monthly payment amount (rounded to cents)

    Raises:
        ValueError: If inputs are invalid
    """
    if principal <= 0:
        raise ValueError("principal must be > 0")
    if annual_rate_pct < 0 or annual_rate_pct > 50:
        raise ValueError("annual_rate_pct must be between 0 and 50")
    if term_months < 1 or term_months > 480:
        raise ValueError("term_months must be between 1 and 480")

    if annual_rate_pct == 0:
        return (principal / Decimal(term_months)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    monthly_rate = annual_rate_pct / Decimal(100) / Decimal(12)

    numerator = principal * monthly_rate * ((1 + monthly_rate) ** term_months)
    denominator = ((1 + monthly_rate) ** term_months) - 1

    payment = (numerator / denominator).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return payment


def calculate_amortization(
    principal: Decimal, annual_rate_pct: Decimal, term_months: int
) -> AmortizationResult:
    """Calculate full amortization schedule.

    Args:
        principal: Loan amount in dollars
        annual_rate_pct: Annual interest rate as percentage
        term_months: Number of months for the loan

    Returns:
        Dictionary with monthly_payment, total_interest, and full schedule
    """
    monthly_payment = calculate_monthly_payment(principal, annual_rate_pct, term_months)
    monthly_rate = Decimal(0)
    if annual_rate_pct > 0:
        monthly_rate = annual_rate_pct / Decimal(100) / Decimal(12)

    schedule: list[AmortizationScheduleEntry] = []
    balance = principal
    total_interest = Decimal(0)

    for month in range(1, term_months + 1):
        interest_payment = (balance * monthly_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        if month == term_months:
            principal_payment = balance
            payment = principal_payment + interest_payment
        else:
            principal_payment = (monthly_payment - interest_payment).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            payment = monthly_payment

        balance = (balance - principal_payment).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_interest = (total_interest + interest_payment).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        schedule.append(
            {
                "month": month,
                "payment": payment,
                "principal": principal_payment,
                "interest": interest_payment,
                "balance": max(Decimal(0), balance),
            }
        )

    return {
        "monthly_payment": monthly_payment,
        "total_interest": total_interest,
        "schedule": schedule,
    }
