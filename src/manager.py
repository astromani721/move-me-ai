"""Manager (orchestrator) agent entrypoint."""

from __future__ import annotations

import re

from agents.housing import find_housing_options
from agents.insurance import estimate_insurance
from agents.lifestyle import assess_lifestyle
from agents.school import assess_school
from models import (
    HousingSearchCriteria,
    PropertyDossier,
    RelocationReport,
    RelocationRequest,
)


class RelocationManager:
    """Coordinates worker-agent outputs into one typed report."""

    def run(self, prompt: str) -> RelocationReport:
        request = RelocationRequest(prompt=prompt)
        zip_match = re.search(r"\b(\d{5})\b", prompt)
        zip_code = zip_match.group(1) if zip_match else "00000"
        criteria = HousingSearchCriteria(zip_code=zip_code)
        housing_options = find_housing_options(criteria=criteria)
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

