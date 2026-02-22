"""External-provider stubs.

These helpers are intentionally minimal placeholders. Replace with real API
clients for Zillow/RentCast, GreatSchools, and Google Places.
"""

from __future__ import annotations


def fetch_listing_stub(address: str) -> dict[str, str]:
    """Return a minimal fake listing payload for local development."""
    return {"address": address, "status": "stub"}
