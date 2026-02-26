"""Tests for the housing specialist agent."""

from agents.housing import find_housing_options
from models import HousingOption, HousingSearchCriteria


def _criteria(**kwargs) -> HousingSearchCriteria:
    defaults = {"zip_code": "10583", "bedrooms": 3, "bathrooms": 1}
    return HousingSearchCriteria(**{**defaults, **kwargs})


# ---------------------------------------------------------------------------
# Return type and structure
# ---------------------------------------------------------------------------


def test_returns_list_of_housing_options() -> None:
    results = find_housing_options(_criteria())
    assert isinstance(results, list)
    assert all(isinstance(r, HousingOption) for r in results)


def test_results_sorted_by_rent_ascending() -> None:
    results = find_housing_options(_criteria())
    rents = [r.monthly_rent_usd for r in results]
    assert rents == sorted(rents)


# ---------------------------------------------------------------------------
# Bedroom filter
# ---------------------------------------------------------------------------


def test_bedroom_filter_exact_match() -> None:
    results = find_housing_options(_criteria(bedrooms=3))
    assert all(r.bedrooms == 3 for r in results)


def test_bedroom_filter_excludes_wrong_count() -> None:
    results = find_housing_options(_criteria(bedrooms=2))
    assert all(r.bedrooms == 2 for r in results)


def test_bedroom_filter_no_match_returns_empty() -> None:
    results = find_housing_options(_criteria(bedrooms=10))
    assert results == []


# ---------------------------------------------------------------------------
# Bathroom filter
# ---------------------------------------------------------------------------


def test_bathroom_filter_minimum_satisfied() -> None:
    results = find_housing_options(_criteria(bathrooms=2))
    assert all(r.bathrooms >= 2 for r in results)


def test_bathroom_default_returns_all_listings() -> None:
    results_default = find_housing_options(_criteria(bathrooms=1))
    results_explicit = find_housing_options(_criteria())
    assert results_default == results_explicit


def test_bathroom_filter_no_match_returns_empty() -> None:
    results = find_housing_options(_criteria(bathrooms=99))
    assert results == []


# ---------------------------------------------------------------------------
# Max rent filter
# ---------------------------------------------------------------------------


def test_max_rent_excludes_over_budget() -> None:
    results = find_housing_options(_criteria(max_rent_usd=5000))
    assert all(r.monthly_rent_usd <= 5000 for r in results)


def test_max_rent_none_applies_no_ceiling() -> None:
    results_no_cap = find_housing_options(_criteria(max_rent_usd=None))
    results_high_cap = find_housing_options(_criteria(max_rent_usd=999_999))
    assert results_no_cap == results_high_cap


def test_max_rent_too_low_returns_empty() -> None:
    results = find_housing_options(_criteria(max_rent_usd=100))
    assert results == []


# ---------------------------------------------------------------------------
# Limit
# ---------------------------------------------------------------------------


def test_limit_caps_results() -> None:
    results = find_housing_options(_criteria(bedrooms=3), limit=1)
    assert len(results) == 1


def test_limit_larger_than_pool_returns_all() -> None:
    results = find_housing_options(_criteria(bedrooms=3), limit=100)
    assert len(results) <= 100


# ---------------------------------------------------------------------------
# Zip code fallback
# ---------------------------------------------------------------------------


def test_unknown_zip_returns_fallback_listings() -> None:
    results = find_housing_options(_criteria(zip_code="99999", bedrooms=3))
    assert len(results) > 0


def test_known_zip_returns_zip_specific_listings() -> None:
    results = find_housing_options(_criteria(zip_code="10583", bedrooms=3))
    assert all("10583" in r.address for r in results)
