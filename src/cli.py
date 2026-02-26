"""Command-line interface for move-me-ai housing search."""

from __future__ import annotations

import argparse
import logging
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from agents.housing import find_housing_options
from logging_config import configure_logging
from models import HousingSearchCriteria

log = logging.getLogger(__name__)
console = Console()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="move-me-ai",
        description="Search for rental properties matching your criteria.",
    )
    parser.add_argument(
        "--zip", required=True, metavar="ZIP_CODE", help="Target zip code (e.g. 10583)"
    )
    parser.add_argument(
        "--bedrooms", type=int, default=3, metavar="N", help="Number of bedrooms (default: 3)"
    )
    parser.add_argument(
        "--bathrooms", type=int, default=1, metavar="N", help="Minimum bathrooms (default: 1)"
    )
    parser.add_argument(
        "--max-rent", type=int, default=None, metavar="USD", help="Maximum monthly rent in USD"
    )
    parser.add_argument(
        "--limit", type=int, default=5, metavar="N", help="Max results to return (default: 5)"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log level",
    )
    return parser


def _render_results(options: list, criteria: HousingSearchCriteria) -> None:
    if not options:
        console.print(
            f"\n[yellow]No listings found for zip [bold]{criteria.zip_code}[/bold] "
            f"({criteria.bedrooms}BR"
            + (f", max ${criteria.max_rent_usd:,}/mo" if criteria.max_rent_usd else "")
            + ")[/yellow]\n"
        )
        return

    table = Table(
        title=f"Housing Results — {criteria.zip_code}  "
              f"({criteria.bedrooms}BR"
              + (f"  ·  max ${criteria.max_rent_usd:,}/mo" if criteria.max_rent_usd else "")
              + ")",
        show_lines=True,
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Address", style="cyan", no_wrap=True)
    table.add_column("Bed", justify="center")
    table.add_column("Bath", justify="center")
    table.add_column("Monthly Rent", justify="right", style="green")

    for i, opt in enumerate(options, start=1):
        table.add_row(
            str(i), opt.address, str(opt.bedrooms), str(opt.bathrooms), f"${opt.monthly_rent_usd:,}"
        )

    console.print()
    console.print(table)
    console.print(f"\n[dim]{len(options)} listing(s) returned.[/dim]\n")


def main() -> None:
    load_dotenv()
    args = _build_parser().parse_args()
    configure_logging(args.log_level)

    criteria = HousingSearchCriteria(
        zip_code=args.zip,
        bedrooms=args.bedrooms,
        bathrooms=args.bathrooms,
        max_rent_usd=args.max_rent,
    )

    log.info(
        "cli invoked",
        extra={
            "zip": criteria.zip_code,
            "bedrooms": criteria.bedrooms,
            "max_rent_usd": criteria.max_rent_usd,
        },
    )

    try:
        options = find_housing_options(criteria=criteria, limit=args.limit)
    except Exception:
        log.exception("housing search failed")
        console.print("[red]Error:[/red] housing search failed — check logs for details.")
        sys.exit(1)

    _render_results(options, criteria)


if __name__ == "__main__":
    main()