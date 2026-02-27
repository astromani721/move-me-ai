"""Factory functions for smolagents CodeAgent wiring."""

from __future__ import annotations

from smolagents import CodeAgent  # type: ignore[import-untyped]
from smolagents.models import Model  # type: ignore[import-untyped]

from tools.providers import (
    assess_lifestyle_amenities,
    assess_school_quality,
    estimate_insurance_cost,
    search_housing,
)

_EXECUTOR_KWARGS = {"timeout_seconds": 300}

_MANAGER_INSTRUCTIONS = """\
You are a relocation planning manager. Given a user's natural-language relocation
request, you must:

1. Extract the zip code, bedroom count, bathroom count, and max rent from the prompt.
   Defaults: bedrooms=3, bathrooms=1, max_rent_usd=0 (no limit).
2. Call search_housing() to find listings.
3. Parse the JSON string result with json.loads().
4. For each property address, call assess_school_quality(), estimate_insurance_cost(),
   and assess_lifestyle_amenities(). Parse each JSON string result with json.loads().
5. Assemble the results into a single JSON object with this structure:
   {
     "request": {"prompt": "<original prompt>"},
     "properties": [
       {
         "housing": {<housing fields>},
         "school": {<school fields>},
         "insurance": {<insurance fields>},
         "lifestyle": {<lifestyle fields>}
       }
     ]
   }
6. Return the JSON string via final_answer().

IMPORTANT RULES:
- Always start your code with: import json
- All tools return JSON *strings*. Always use json.loads() to parse them before
  accessing fields.
- You can ONLY use these tools: search_housing, assess_school_quality,
  estimate_insurance_cost, assess_lifestyle_amenities, final_answer.
- Do NOT call visit_webpage, web_search, or any other tool.
- Do NOT try to access the internet or visit URLs.
"""


def create_manager_agent(model: Model) -> CodeAgent:
    """Create a single CodeAgent with all tools directly available."""
    return CodeAgent(
        tools=[
            search_housing,
            assess_school_quality,
            estimate_insurance_cost,
            assess_lifestyle_amenities,
        ],
        model=model,
        additional_authorized_imports=["json", "re"],
        max_steps=10,
        instructions=_MANAGER_INSTRUCTIONS,
        verbosity_level=1,
        executor_kwargs=_EXECUTOR_KWARGS,
    )
