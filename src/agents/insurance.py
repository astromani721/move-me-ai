"""Insurance specialist agent placeholder logic."""

from __future__ import annotations

from models import InsuranceEstimate


def estimate_insurance(address: str) -> InsuranceEstimate:
    """Return a mock combined auto+renter estimate for an address."""
    return InsuranceEstimate(address=address, auto_renters_monthly_usd=210)

