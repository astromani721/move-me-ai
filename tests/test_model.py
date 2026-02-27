"""Tests for the model factory."""

from unittest.mock import patch

import pytest
from smolagents import InferenceClientModel, OpenAIServerModel

from model import get_model


def test_get_model_raises_when_model_id_missing() -> None:
    env = {"MODEL_PROVIDER": "huggingface"}
    with patch.dict("os.environ", env, clear=True), \
            pytest.raises(RuntimeError, match="MODEL_ID is not set"):
        get_model()


def test_get_model_raises_when_hf_token_missing() -> None:
    env = {"MODEL_PROVIDER": "huggingface", "MODEL_ID": "some/model"}
    with patch.dict("os.environ", env, clear=True), \
            pytest.raises(RuntimeError, match="HUGGINGFACEHUB_API_TOKEN"):
        get_model()


def test_get_model_returns_inference_client_model() -> None:
    env = {
        "MODEL_PROVIDER": "huggingface",
        "HUGGINGFACEHUB_API_TOKEN": "hf_test",
        "MODEL_ID": "Qwen/Qwen2.5-Coder-32B-Instruct",
    }
    with patch.dict("os.environ", env, clear=True):
        model = get_model()
    assert isinstance(model, InferenceClientModel)


def test_get_model_uses_model_id_from_env() -> None:
    env = {
        "MODEL_PROVIDER": "huggingface",
        "HUGGINGFACEHUB_API_TOKEN": "hf_test",
        "MODEL_ID": "some/other-model",
    }
    with patch.dict("os.environ", env, clear=True):
        model = get_model()
    assert model.model_id == "some/other-model"


def test_get_model_ollama_returns_openai_server_model() -> None:
    env = {"MODEL_PROVIDER": "ollama", "MODEL_ID": "qwen2.5-coder:14b"}
    with patch.dict("os.environ", env, clear=True):
        model = get_model()
    assert isinstance(model, OpenAIServerModel)
    assert model.model_id == "qwen2.5-coder:14b"


def test_get_model_unknown_provider_raises() -> None:
    env = {"MODEL_PROVIDER": "bogus", "MODEL_ID": "some-model"}
    with patch.dict("os.environ", env, clear=True), \
            pytest.raises(ValueError, match="Unknown MODEL_PROVIDER"):
        get_model()
