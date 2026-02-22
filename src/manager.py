"""Manager (orchestrator) agent entrypoint."""

from __future__ import annotations

from src.agents.housing import find_housing_options
from src.agents.insurance import estimate_insurance
from src.agents.lifestyle import assess_lifestyle
from src.agents.school import assess_school
from src.models import PropertyDossier, RelocationReport, RelocationRequest


class RelocationManager:
    """Coordinates worker-agent outputs into one typed report."""

    def run(self, prompt: str) -> RelocationReport:
        request = RelocationRequest(prompt=prompt)
        housing_options = find_housing_options(request=request)
        dossiers = []
        for option in housing_options:
            dossiers.append(
                PropertyDossier(
                    housing=option,
                    school=assess_school(address=option.address),
                    insurance=estimate_insurance(address=option.address),
                    lifestyle=assess_lifestyle(address=option.address),
                )
            )
        return RelocationReport(request=request, properties=dossiers)


relocation_manager = RelocationManager()

