"""Lifestyle specialist agent placeholder logic."""

from __future__ import annotations

from src.models import LifestyleAssessment


def assess_lifestyle(address: str) -> LifestyleAssessment:
    """Return mock amenity signals for an address."""
    return LifestyleAssessment(
        address=address,
        nearest_indian_or_asian_grocery="Sample Asian Market",
        grocery_distance_miles=1.2,
        nearest_park="Sample Central Park",
        nearest_library="Sample Public Library",
    )

