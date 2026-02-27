"""Command-line interface for move-me-ai relocation planner."""

from __future__ import annotations

import argparse
import logging
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from logging_config import configure_logging
from manager import RelocationManager
from models import RelocationReport

log = logging.getLogger(__name__)
console = Console()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="move-me-ai",
        description="Autonomous relocation planner — describe your move and get a full report.",
    )
    parser.add_argument(
        "prompt",
        help='Natural language relocation request (e.g. "Relocating to 10583, 3BR, max $5000/mo")',
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log level",
    )
    parser.add_argument(
        "--agent",
        action="store_true",
        default=False,
        help="Use smolagents CodeAgent pipeline instead of direct function calls",
    )
    return parser


def _render_report(report: RelocationReport) -> None:
    if not report.properties:
        console.print("\n[yellow]No properties found for your request.[/yellow]\n")
        return

    table = Table(
        title=f"Relocation Report — {report.request.prompt}",
        show_lines=True,
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Address", style="cyan", no_wrap=True)
    table.add_column("Bed", justify="center")
    table.add_column("Bath", justify="center")
    table.add_column("Rent/mo", justify="right", style="green")
    table.add_column("School", no_wrap=True)
    table.add_column("Rating", justify="center")
    table.add_column("Insurance/mo", justify="right")
    table.add_column("Nearest Grocery", no_wrap=True)

    for i, dossier in enumerate(report.properties, start=1):
        h = dossier.housing
        s = dossier.school
        ins = dossier.insurance
        lf = dossier.lifestyle
        table.add_row(
            str(i),
            h.address,
            str(h.bedrooms),
            str(h.bathrooms),
            f"${h.monthly_rent_usd:,}",
            s.school_name,
            f"{s.rating_out_of_10}/10",
            f"${ins.auto_renters_monthly_usd:,}",
            f"{lf.nearest_indian_or_asian_grocery} ({lf.grocery_distance_miles}mi)",
        )

    console.print()
    console.print(table)
    console.print(f"\n[dim]{len(report.properties)} propert(ies) returned.[/dim]\n")


def main() -> None:
    load_dotenv()
    args = _build_parser().parse_args()
    configure_logging(args.log_level)

    log.info("cli invoked", extra={"prompt": args.prompt})

    manager = RelocationManager(use_agent=args.agent)

    try:
        report = manager.run(args.prompt)
    except Exception:
        log.exception("relocation report failed")
        console.print("[red]Error:[/red] relocation report failed — check logs for details.")
        sys.exit(1)

    _render_report(report)


if __name__ == "__main__":
    main()
