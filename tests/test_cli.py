"""Tests for the CLI argument parsing and output rendering."""

from unittest.mock import patch

import pytest
from rich.console import Console

from cli import _build_parser, _render_report
from models import (
    HousingOption,
    InsuranceEstimate,
    LifestyleAssessment,
    PropertyDossier,
    RelocationReport,
    RelocationRequest,
    SchoolAssessment,
)


def _dossier(**kwargs) -> PropertyDossier:
    defaults = dict(
        housing=HousingOption(address="1 Test St", monthly_rent_usd=3000, bedrooms=3, bathrooms=1),
        school=SchoolAssessment(address="1 Test St", school_name="Test High", rating_out_of_10=9.0),
        insurance=InsuranceEstimate(address="1 Test St", auto_renters_monthly_usd=200),
        lifestyle=LifestyleAssessment(
            address="1 Test St",
            nearest_indian_or_asian_grocery="Test Market",
            grocery_distance_miles=0.8,
            nearest_park="Test Park",
            nearest_library="Test Library",
        ),
    )
    return PropertyDossier(**{**defaults, **kwargs})


def _report(dossiers: list | None = None) -> RelocationReport:
    return RelocationReport(
        request=RelocationRequest(prompt="Relocating to 10583"),
        properties=dossiers if dossiers is not None else [_dossier()],
    )


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def test_parser_requires_prompt() -> None:
    parser = _build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_parser_accepts_prompt() -> None:
    parser = _build_parser()
    args = parser.parse_args(["Relocating to 10583, 3BR"])
    assert args.prompt == "Relocating to 10583, 3BR"
    assert args.log_level == "INFO"


def test_parser_rejects_invalid_log_level() -> None:
    parser = _build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["some prompt", "--log-level", "VERBOSE"])


# ---------------------------------------------------------------------------
# Render report
# ---------------------------------------------------------------------------


def test_render_report_prints_table(capsys) -> None:
    console = Console(highlight=False, width=200)
    with patch("cli.console", console):
        _render_report(_report([_dossier()]))
    captured = capsys.readouterr()
    assert "1 Test St" in captured.out
    assert "3,000" in captured.out


def test_render_report_shows_all_columns(capsys) -> None:
    console = Console(highlight=False, width=200)
    with patch("cli.console", console):
        _render_report(_report([_dossier()]))
    captured = capsys.readouterr()
    assert "School" in captured.out
    assert "Insurance/mo" in captured.out
    assert "Grocery" in captured.out


def test_render_report_no_properties_prints_warning(capsys) -> None:
    console = Console(highlight=False, width=200)
    with patch("cli.console", console):
        _render_report(_report([]))
    captured = capsys.readouterr()
    assert "No properties found" in captured.out


# ---------------------------------------------------------------------------
# main() entry point
# ---------------------------------------------------------------------------


def test_main_runs_end_to_end(capsys) -> None:
    console = Console(highlight=False, width=200)
    prompt = "Relocating to 10583, 3 bedrooms"
    with patch("cli.console", console), patch("sys.argv", ["cli", prompt]):
        from cli import main
        main()
    captured = capsys.readouterr()
    assert "10583" in captured.out
    assert "Rent/mo" in captured.out
