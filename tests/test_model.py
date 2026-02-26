"""Tests for the HuggingFace model factory."""

from unittest.mock import patch

import pytest
from smolagents import InferenceClientModel

from model import get_model


def test_get_model_raises_when_token_missing() -> None:
    with patch.dict("os.environ", {}, clear=True), \
            pytest.raises(RuntimeError, match="HUGGINGFACEHUB_API_TOKEN"):
        get_model()


def test_get_model_returns_inference_client_model() -> None:
    env = {"HUGGINGFACEHUB_API_TOKEN": "hf_test", "MODEL_ID": "Qwen/Qwen2.5-Coder-32B-Instruct"}
    with patch.dict("os.environ", env):
        model = get_model()
    assert isinstance(model, InferenceClientModel)


def test_get_model_uses_model_id_from_env() -> None:
    env = {"HUGGINGFACEHUB_API_TOKEN": "hf_test", "MODEL_ID": "some/other-model"}
    with patch.dict("os.environ", env):
        model = get_model()
    assert model.model_id == "some/other-model"


def test_get_model_uses_default_model_id_when_not_set() -> None:
    env = {"HUGGINGFACEHUB_API_TOKEN": "hf_test"}
    with patch.dict("os.environ", env, clear=False):
        # Remove MODEL_ID if present
        env_without_model = {k: v for k, v in __import__("os").environ.items() if k != "MODEL_ID"}
        with patch.dict("os.environ", env_without_model, clear=True):
            model = get_model()
    assert model.model_id == "Qwen/Qwen2.5-Coder-32B-Instruct"
