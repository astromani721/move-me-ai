from src.manager import relocation_manager
from src.models import RelocationReport


def test_manager_run_returns_report() -> None:
    report = relocation_manager.run(
        "Relocating to 10583. Find 3 houses and basic schooling plus amenities."
    )
    assert isinstance(report, RelocationReport)
    assert len(report.properties) == 3


def test_report_addresses_stay_consistent_across_specialists() -> None:
    report = relocation_manager.run("Find relocation options.")
    first = report.properties[0]
    assert first.housing.address == first.school.address
    assert first.housing.address == first.insurance.address
    assert first.housing.address == first.lifestyle.address

