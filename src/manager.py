"""Manager (orchestrator) agent entrypoint."""

from __future__ import annotations

import json
import logging
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from smolagents import CodeAgent  # type: ignore[import-untyped]

from agents.housing import find_housing_options
from agents.insurance import estimate_insurance
from agents.lifestyle import assess_lifestyle
from agents.school import assess_school
from models import (
    HousingOption,
    HousingSearchCriteria,
    InsuranceEstimate,
    LifestyleAssessment,
    PropertyDossier,
    RelocationReport,
    RelocationRequest,
    SchoolAssessment,
)

log = logging.getLogger(__name__)


class RelocationManager:
    """Coordinates worker-agent outputs into one typed report.

    Supports two modes:
    - direct (default): calls agent functions directly — fast, no LLM needed.
    - agent (use_agent=True): delegates to a smolagents CodeAgent pipeline.
    """

    def __init__(self, *, use_agent: bool = False) -> None:
        self._use_agent = use_agent
        self._agent: CodeAgent | None = None  # lazy-init for agent mode

    def run(self, prompt: str) -> RelocationReport:
        if self._use_agent:
            return self._run_agent(prompt)
        return self._run_direct(prompt)

    def _run_direct(self, prompt: str) -> RelocationReport:
        """Original direct-call orchestration (no LLM)."""
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

    def _run_agent(self, prompt: str) -> RelocationReport:
        """Delegate to smolagents CodeAgent pipeline."""
        if self._agent is None:
            from agent_factory import create_manager_agent
            from model import get_model

            log.info("initializing smolagents CodeAgent pipeline")
            self._agent = create_manager_agent(get_model())

        log.info("running agent pipeline", extra={"prompt": prompt})
        raw = self._agent.run(prompt)
        return _parse_agent_output(raw, prompt)


def _parse_agent_output(raw: object, prompt: str) -> RelocationReport:
    """Convert CodeAgent output (dict or JSON string) into a typed RelocationReport."""
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            log.warning("agent returned non-JSON string, wrapping as empty report")
            return RelocationReport(
                request=RelocationRequest(prompt=prompt), properties=[]
            )
    elif isinstance(raw, dict):
        data = raw
    else:
        log.warning("agent returned unexpected type %s, wrapping as empty report", type(raw))
        return RelocationReport(
            request=RelocationRequest(prompt=prompt), properties=[]
        )

    # If data already matches RelocationReport structure, parse directly
    if "request" in data and "properties" in data:
        try:
            return RelocationReport.model_validate(data)
        except Exception:
            log.warning("agent output failed RelocationReport validation, building manually")

    # Try to build from a flat list of properties
    properties_raw = data.get("properties", [])
    dossiers = []
    for prop in properties_raw:
        try:
            dossiers.append(
                PropertyDossier(
                    housing=HousingOption.model_validate(prop.get("housing", {})),
                    school=SchoolAssessment.model_validate(prop.get("school", {})),
                    insurance=InsuranceEstimate.model_validate(prop.get("insurance", {})),
                    lifestyle=LifestyleAssessment.model_validate(prop.get("lifestyle", {})),
                )
            )
        except Exception:
            log.warning("skipping malformed property dossier: %s", prop)

    return RelocationReport(
        request=RelocationRequest(prompt=prompt),
        properties=dossiers,
    )


relocation_manager = RelocationManager()
