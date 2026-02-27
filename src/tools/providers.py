"""Tool-decorated provider functions for smolagents integration.

Each function wraps an existing agent stub and returns a JSON string
so that CodeAgent can parse results in its sandbox.
"""

from __future__ import annotations

import json

from smolagents import tool  # type: ignore[import-untyped]

from agents.housing import find_housing_options
from agents.insurance import estimate_insurance
from agents.lifestyle import assess_lifestyle
from agents.school import assess_school
from models import HousingSearchCriteria


@tool
def search_housing(
    zip_code: str,
    bedrooms: int = 3,
    bathrooms: int = 1,
    max_rent_usd: int = 0,
    limit: int = 5,
) -> str:
    """Search for rental housing options in a given zip code.

    Args:
        zip_code: Five-digit US zip code to search in.
        bedrooms: Number of bedrooms required.
        bathrooms: Minimum number of bathrooms required. Must be >= 1.
        max_rent_usd: Maximum monthly rent in USD. Use 0 for no limit.
        limit: Maximum number of results to return.

    Returns:
        A JSON string. Use json.loads() to parse it into a list of dicts,
        each with keys: address, monthly_rent_usd, bedrooms, bathrooms.
    """
    bathrooms = max(bathrooms or 1, 1)
    rent = max_rent_usd if isinstance(max_rent_usd, int) and max_rent_usd > 0 else None
    criteria = HousingSearchCriteria(
        zip_code=zip_code,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        max_rent_usd=rent,
    )
    options = find_housing_options(criteria=criteria, limit=limit)
    return json.dumps([opt.model_dump() for opt in options])


@tool
def assess_school_quality(address: str) -> str:
    """Assess school quality near a given address.

    Args:
        address: Full street address to evaluate.

    Returns:
        A JSON string. Use json.loads() to parse it into a dict with keys:
        address, school_name, rating_out_of_10.
    """
    result = assess_school(address=address)
    return json.dumps(result.model_dump())


@tool
def estimate_insurance_cost(address: str) -> str:
    """Estimate combined auto and renters insurance cost for an address.

    Args:
        address: Full street address to evaluate.

    Returns:
        A JSON string. Use json.loads() to parse it into a dict with keys:
        address, auto_renters_monthly_usd.
    """
    result = estimate_insurance(address=address)
    return json.dumps(result.model_dump())


@tool
def assess_lifestyle_amenities(address: str) -> str:
    """Assess lifestyle amenities near a given address including groceries, parks, libraries.

    Args:
        address: Full street address to evaluate.

    Returns:
        A JSON string. Use json.loads() to parse it into a dict with keys:
        address, nearest_indian_or_asian_grocery, grocery_distance_miles,
        nearest_park, nearest_library.
    """
    result = assess_lifestyle(address=address)
    return json.dumps(result.model_dump())
