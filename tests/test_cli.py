"""Tests for the CLI argument parsing and output rendering."""

from unittest.mock import patch

import pytest
from rich.console import Console

from cli import _build_parser, _render_results
from models import HousingOption, HousingSearchCriteria


def _option(**kwargs) -> HousingOption:
    defaults = {"address": "1 Test St", "monthly_rent_usd": 3000, "bedrooms": 3, "bathrooms": 1}
    return HousingOption(**{**defaults, **kwargs})


def _criteria(**kwargs) -> HousingSearchCriteria:
    defaults = {"zip_code": "10583", "bedrooms": 3, "bathrooms": 1}
    return HousingSearchCriteria(**{**defaults, **kwargs})


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def test_parser_requires_zip() -> None:
    parser = _build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_parser_defaults() -> None:
    parser = _build_parser()
    args = parser.parse_args(["--zip", "10583"])
    assert args.zip == "10583"
    assert args.bedrooms == 3
    assert args.bathrooms == 1
    assert args.max_rent is None
    assert args.limit == 5
    assert args.log_level == "INFO"


def test_parser_accepts_all_flags() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        ["--zip", "10583", "--bedrooms", "2", "--bathrooms", "2",
         "--max-rent", "4000", "--limit", "3"]
    )
    assert args.zip == "10583"
    assert args.bedrooms == 2
    assert args.bathrooms == 2
    assert args.max_rent == 4000
    assert args.limit == 3


def test_parser_rejects_invalid_log_level() -> None:
    parser = _build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--zip", "10583", "--log-level", "VERBOSE"])


# ---------------------------------------------------------------------------
# Render results
# ---------------------------------------------------------------------------


def test_render_results_prints_table(capsys) -> None:
    console = Console(highlight=False)
    options = [_option(address="88 Post Rd", monthly_rent_usd=4800)]
    with patch("cli.console", console):
        _render_results(options, _criteria())
    captured = capsys.readouterr()
    assert "88 Post Rd" in captured.out
    assert "4,800" in captured.out


def test_render_no_results_prints_warning(capsys) -> None:
    console = Console(highlight=False)
    with patch("cli.console", console):
        _render_results([], _criteria())
    captured = capsys.readouterr()
    assert "No listings found" in captured.out


def test_render_shows_bath_column(capsys) -> None:
    console = Console(highlight=False)
    options = [_option(bathrooms=2)]
    with patch("cli.console", console):
        _render_results(options, _criteria())
    captured = capsys.readouterr()
    assert "Bath" in captured.out


# ---------------------------------------------------------------------------
# main() entry point
# ---------------------------------------------------------------------------


def test_main_runs_and_prints_results(capsys) -> None:
    console = Console(highlight=False)
    with patch("cli.console", console), \
            patch("sys.argv", ["cli", "--zip", "10583", "--bedrooms", "3"]):
        from cli import main
        main()
    captured = capsys.readouterr()
    assert "10583" in captured.out
    assert "Monthly Rent" in captured.out
