"""FastAPI application for amortization calculations."""

import json
import logging
import sys
from decimal import Decimal
from os import getenv
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .calculator import calculate_amortization


class AmortizationRequest(BaseModel):
    principal: Decimal = Field(..., gt=0, description="Loan amount in dollars")
    annual_rate_pct: Decimal = Field(
        ..., ge=0, le=50, description="Annual interest rate as percentage"
    )
    term_months: int = Field(..., ge=1, le=480, description="Loan term in months")


class ScheduleEntry(BaseModel):
    month: int
    payment: Decimal
    principal: Decimal
    interest: Decimal
    balance: Decimal


class AmortizationResponse(BaseModel):
    monthly_payment: Decimal
    total_interest: Decimal
    schedule: list[ScheduleEntry]


def setup_logging() -> None:
    """Configure structured JSON logging."""
    log_level = getenv("LOG_LEVEL", "INFO").upper()

    class JSONFormatter(logging.Formatter):
        def format(self, record: Any) -> str:
            log_data = {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }
            if record.exc_info:
                log_data["exception"] = self.formatException(record.exc_info)
            return json.dumps(log_data)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logging.basicConfig(level=log_level, handlers=[handler])


setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(title="Amortization Service", version="0.1.0")


@app.post("/v1/amortization", response_model=AmortizationResponse)
async def amortize(request: AmortizationRequest) -> AmortizationResponse:
    """Calculate amortization schedule.

    Args:
        request: Loan parameters (principal, annual_rate_pct, term_months)

    Returns:
        Monthly payment, total interest, and full amortization schedule
    """
    logger.info(
        "Amortization request",
        extra={
            "principal": str(request.principal),
            "annual_rate_pct": str(request.annual_rate_pct),
            "term_months": request.term_months,
        },
    )

    try:
        result = calculate_amortization(
            request.principal, request.annual_rate_pct, request.term_months
        )
        schedule = [ScheduleEntry(**entry) for entry in result["schedule"]]
        response = AmortizationResponse(
            monthly_payment=result["monthly_payment"],
            total_interest=result["total_interest"],
            schedule=schedule,
        )
        logger.info(
            "Amortization calculated successfully",
            extra={"monthly_payment": str(response.monthly_payment)},
        )
        return response
    except ValueError as e:
        logger.error("Validation error", extra={"error": str(e)})
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    """Readiness probe."""
    return {"status": "ready"}
