"""Model factory — returns a ready-to-use smolagents Model.

Supports two providers controlled by MODEL_PROVIDER env var:
  - "huggingface" (default): HuggingFace Inference API
  - "ollama": Local Ollama server

All configuration lives in .env:
  - MODEL_PROVIDER: "huggingface" or "ollama"
  - MODEL_ID: model name (required)
  - HUGGINGFACEHUB_API_TOKEN: required for huggingface provider
  - OLLAMA_BASE_URL: optional, defaults to http://localhost:11434/v1
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from smolagents import InferenceClientModel, OpenAIServerModel  # type: ignore[import-untyped]
from smolagents.models import Model  # type: ignore[import-untyped]

load_dotenv()

_DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434/v1"


def get_model() -> Model:
    """Return a Model instance based on MODEL_PROVIDER env var.

    Raises:
        RuntimeError: If required env vars are missing.
        ValueError: If MODEL_PROVIDER is not recognized.
    """
    provider = os.getenv("MODEL_PROVIDER", "huggingface").lower()
    model_id = os.getenv("MODEL_ID")
    if not model_id:
        raise RuntimeError(
            "MODEL_ID is not set. Add it to your .env file and try again."
        )

    if provider == "ollama":
        api_base = os.getenv("OLLAMA_BASE_URL", _DEFAULT_OLLAMA_BASE_URL)
        return OpenAIServerModel(
            model_id=model_id,
            api_base=api_base,
            api_key="ollama",
        )

    if provider == "huggingface":
        token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if not token:
            raise RuntimeError(
                "HUGGINGFACEHUB_API_TOKEN is not set. "
                "Add it to your .env file and try again."
            )
        return InferenceClientModel(model_id=model_id, token=token)

    raise ValueError(
        f"Unknown MODEL_PROVIDER '{provider}'. Use 'huggingface' or 'ollama'."
    )
