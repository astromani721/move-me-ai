"""Housing specialist agent — returns listings matching search criteria."""

from __future__ import annotations

import logging

from models import HousingOption, HousingSearchCriteria

log = logging.getLogger(__name__)

# Stub dataset keyed by zip code.  Replace with RentCast API call later.
_STUB_LISTINGS: dict[str, list[HousingOption]] = {
    "10583": [
        HousingOption(
            address="14 Weaver St, Scarsdale, NY 10583",
            monthly_rent_usd=5200, bedrooms=3, bathrooms=2,
        ),
        HousingOption(
            address="88 Post Rd, Scarsdale, NY 10583",
            monthly_rent_usd=4800, bedrooms=3, bathrooms=1,
        ),
        HousingOption(
            address="3 Mamaroneck Rd, Scarsdale, NY 10583",
            monthly_rent_usd=6000, bedrooms=3, bathrooms=2,
        ),
        HousingOption(
            address="22 Garth Rd, Scarsdale, NY 10583",
            monthly_rent_usd=4200, bedrooms=2, bathrooms=1,
        ),
    ],
}
_FALLBACK_LISTINGS: list[HousingOption] = [
    HousingOption(address="123 Oak Ave", monthly_rent_usd=3200, bedrooms=3, bathrooms=1),
    HousingOption(address="42 Maple St", monthly_rent_usd=2950, bedrooms=3, bathrooms=1),
    HousingOption(address="9 River Rd", monthly_rent_usd=3400, bedrooms=3, bathrooms=2),
]


def find_housing_options(criteria: HousingSearchCriteria, limit: int = 5) -> list[HousingOption]:
    """Return listings that match the given search criteria.

    Filters by bedroom count and optional rent ceiling.
    Results are sorted by monthly rent ascending.
    """
    log.info(
        "housing search started",
        extra={
            "zip_code": criteria.zip_code,
            "bedrooms": criteria.bedrooms,
            "bathrooms": criteria.bathrooms,
            "max_rent_usd": criteria.max_rent_usd,
        },
    )

    candidates = _STUB_LISTINGS.get(criteria.zip_code, _FALLBACK_LISTINGS)

    results = [
        opt for opt in candidates
        if opt.bedrooms == criteria.bedrooms
        and opt.bathrooms >= criteria.bathrooms
        and (criteria.max_rent_usd is None or opt.monthly_rent_usd <= criteria.max_rent_usd)
    ]
    results.sort(key=lambda o: o.monthly_rent_usd)
    results = results[:limit]

    log.info("housing search complete", extra={"matches": len(results)})
    return results