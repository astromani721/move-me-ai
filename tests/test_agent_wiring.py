"""Tests for smolagents wiring: @tool functions, agent output parsing, and dual-mode manager."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from manager import RelocationManager, _parse_agent_output
from models import RelocationReport
from tools.providers import (
    assess_lifestyle_amenities,
    assess_school_quality,
    estimate_insurance_cost,
    search_housing,
)

# ---------------------------------------------------------------------------
# TestToolFunctions — call each @tool function directly, verify JSON output
# ---------------------------------------------------------------------------


class TestToolFunctions:
    def test_search_housing_returns_valid_json(self) -> None:
        result = search_housing("10583", bedrooms=3, bathrooms=1, max_rent_usd=0, limit=5)
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0
        assert "address" in data[0]
        assert "monthly_rent_usd" in data[0]

    def test_search_housing_respects_limit(self) -> None:
        result = search_housing("10583", bedrooms=3, bathrooms=1, max_rent_usd=0, limit=1)
        data = json.loads(result)
        assert len(data) == 1

    def test_assess_school_quality_returns_valid_json(self) -> None:
        result = assess_school_quality("14 Weaver St, Scarsdale, NY 10583")
        data = json.loads(result)
        assert "school_name" in data
        assert "rating_out_of_10" in data
        assert data["address"] == "14 Weaver St, Scarsdale, NY 10583"

    def test_estimate_insurance_cost_returns_valid_json(self) -> None:
        result = estimate_insurance_cost("14 Weaver St, Scarsdale, NY 10583")
        data = json.loads(result)
        assert "auto_renters_monthly_usd" in data
        assert data["address"] == "14 Weaver St, Scarsdale, NY 10583"

    def test_assess_lifestyle_amenities_returns_valid_json(self) -> None:
        result = assess_lifestyle_amenities("14 Weaver St, Scarsdale, NY 10583")
        data = json.loads(result)
        assert "nearest_indian_or_asian_grocery" in data
        assert "nearest_park" in data
        assert "nearest_library" in data


# ---------------------------------------------------------------------------
# TestParseAgentOutput — test _parse_agent_output with various inputs
# ---------------------------------------------------------------------------


class TestParseAgentOutput:
    def _make_report_dict(self) -> dict:
        return {
            "request": {"prompt": "test prompt"},
            "properties": [
                {
                    "housing": {
                        "address": "123 Oak Ave",
                        "monthly_rent_usd": 3200,
                        "bedrooms": 3,
                        "bathrooms": 1,
                    },
                    "school": {
                        "address": "123 Oak Ave",
                        "school_name": "Test School",
                        "rating_out_of_10": 8.0,
                    },
                    "insurance": {
                        "address": "123 Oak Ave",
                        "auto_renters_monthly_usd": 200,
                    },
                    "lifestyle": {
                        "address": "123 Oak Ave",
                        "nearest_indian_or_asian_grocery": "Test Market",
                        "grocery_distance_miles": 1.5,
                        "nearest_park": "Test Park",
                        "nearest_library": "Test Library",
                    },
                }
            ],
        }

    def test_parse_dict_input(self) -> None:
        data = self._make_report_dict()
        report = _parse_agent_output(data, "test prompt")
        assert isinstance(report, RelocationReport)
        assert len(report.properties) == 1
        assert report.properties[0].housing.address == "123 Oak Ave"

    def test_parse_json_string_input(self) -> None:
        data = self._make_report_dict()
        report = _parse_agent_output(json.dumps(data), "test prompt")
        assert isinstance(report, RelocationReport)
        assert len(report.properties) == 1

    def test_parse_empty_properties(self) -> None:
        data = {"request": {"prompt": "test"}, "properties": []}
        report = _parse_agent_output(data, "test")
        assert isinstance(report, RelocationReport)
        assert len(report.properties) == 0

    def test_parse_invalid_string_returns_empty_report(self) -> None:
        report = _parse_agent_output("not valid json at all", "test")
        assert isinstance(report, RelocationReport)
        assert len(report.properties) == 0

    def test_parse_unexpected_type_returns_empty_report(self) -> None:
        report = _parse_agent_output(42, "test")  # type: ignore[arg-type]
        assert isinstance(report, RelocationReport)
        assert len(report.properties) == 0


# ---------------------------------------------------------------------------
# TestAgentModeWithMock — mock CodeAgent, verify manager dispatches correctly
# ---------------------------------------------------------------------------


class TestAgentModeWithMock:
    def test_agent_mode_calls_agent_and_parses_output(self) -> None:
        report_dict = {
            "request": {"prompt": "Move to 10583"},
            "properties": [
                {
                    "housing": {
                        "address": "14 Weaver St",
                        "monthly_rent_usd": 5200,
                        "bedrooms": 3,
                        "bathrooms": 2,
                    },
                    "school": {
                        "address": "14 Weaver St",
                        "school_name": "Scarsdale HS",
                        "rating_out_of_10": 9.0,
                    },
                    "insurance": {
                        "address": "14 Weaver St",
                        "auto_renters_monthly_usd": 210,
                    },
                    "lifestyle": {
                        "address": "14 Weaver St",
                        "nearest_indian_or_asian_grocery": "Patel Brothers",
                        "grocery_distance_miles": 2.1,
                        "nearest_park": "Chase Park",
                        "nearest_library": "Scarsdale Library",
                    },
                }
            ],
        }

        mock_agent = MagicMock()
        mock_agent.run.return_value = json.dumps(report_dict)

        manager = RelocationManager(use_agent=True)
        manager._agent = mock_agent  # inject mock, skip lazy init

        report = manager.run("Move to 10583")
        assert isinstance(report, RelocationReport)
        assert len(report.properties) == 1
        assert report.properties[0].housing.address == "14 Weaver St"
        mock_agent.run.assert_called_once_with("Move to 10583")


# ---------------------------------------------------------------------------
# TestDirectModeUnchanged — regression: direct mode still works
# ---------------------------------------------------------------------------


class TestDirectModeUnchanged:
    def test_direct_mode_returns_report(self) -> None:
        manager = RelocationManager(use_agent=False)
        report = manager.run("Relocating to 10583. Find rentals.")
        assert isinstance(report, RelocationReport)
        assert len(report.properties) > 0

    def test_singleton_still_works(self) -> None:
        from manager import relocation_manager

        report = relocation_manager.run("Find relocation options.")
        assert isinstance(report, RelocationReport)
