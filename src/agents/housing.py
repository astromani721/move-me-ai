"""Housing specialist agent placeholder logic."""

from __future__ import annotations

from src.models import HousingOption, RelocationRequest


def find_housing_options(request: RelocationRequest, limit: int = 3) -> list[HousingOption]:
    """Return a deterministic starter set of housing options.

    This is a temporary stub until live listing APIs are integrated.
    """
    _ = request
    sample = [
        HousingOption(address="123 Oak Ave", monthly_rent_usd=3200, bedrooms=3),
        HousingOption(address="42 Maple St", monthly_rent_usd=2950, bedrooms=3),
        HousingOption(address="9 River Rd", monthly_rent_usd=3400, bedrooms=3),
    ]
    return sample[:limit]
