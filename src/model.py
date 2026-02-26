"""HuggingFace model factory — returns a ready-to-use InferenceClientModel."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from smolagents import InferenceClientModel  # type: ignore[import-untyped]

load_dotenv()

_DEFAULT_MODEL_ID = "Qwen/Qwen2.5-Coder-32B-Instruct"


def get_model() -> InferenceClientModel:
    """Return an InferenceClientModel loaded from environment variables.

    Raises:
        RuntimeError: If HUGGINGFACEHUB_API_TOKEN is not set.
    """
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        raise RuntimeError(
            "HUGGINGFACEHUB_API_TOKEN is not set. "
            "Add it to your .env file and try again."
        )
    model_id = os.getenv("MODEL_ID", _DEFAULT_MODEL_ID)
    return InferenceClientModel(model_id=model_id, token=token)
