"""Typed data contracts shared across manager and worker agents."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HousingSearchCriteria(BaseModel):
    """Structured search parameters used by the housing specialist."""

    zip_code: str
    bedrooms: int = Field(default=3, ge=1)
    bathrooms: int = Field(default=1, ge=1)
    max_rent_usd: int | None = Field(default=None, ge=0)


class RelocationRequest(BaseModel):
    """Normalized user input passed to the orchestration layer."""

    prompt: str = Field(min_length=1)


class HousingOption(BaseModel):
    """A candidate property selected by the housing specialist."""

    address: str
    monthly_rent_usd: int
    bedrooms: int
    bathrooms: int


class SchoolAssessment(BaseModel):
    """School quality signal associated with an address."""

    address: str
    school_name: str
    rating_out_of_10: float


class InsuranceEstimate(BaseModel):
    """Insurance estimate for the selected address."""

    address: str
    auto_renters_monthly_usd: int


class LifestyleAssessment(BaseModel):
    """Nearby amenities and livability signals."""

    address: str
    nearest_indian_or_asian_grocery: str
    grocery_distance_miles: float
    nearest_park: str
    nearest_library: str


class PropertyDossier(BaseModel):
    """Per-property aggregate assembled by the manager."""

    housing: HousingOption
    school: SchoolAssessment
    insurance: InsuranceEstimate
    lifestyle: LifestyleAssessment


class RelocationReport(BaseModel):
    """Final manager output for a relocation run."""

    request: RelocationRequest
    properties: list[PropertyDossier]
