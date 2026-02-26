"""School specialist agent placeholder logic."""

from __future__ import annotations

from models import SchoolAssessment


def assess_school(address: str) -> SchoolAssessment:
    """Return a mock school assessment for an address."""
    return SchoolAssessment(
        address=address,
        school_name="Sample Public High School",
        rating_out_of_10=8.8,
    )

