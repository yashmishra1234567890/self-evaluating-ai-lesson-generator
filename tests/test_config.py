
import pytest

from config import get_settings, validate_settings


def test_configuration_loading(monkeypatch):

    monkeypatch.setenv(
        "OPENROUTER_API_KEY",
        "test-api-key"
    )

    monkeypatch.setenv(
        "OPENROUTER_MODEL",
        "test-model"
    )

    settings = get_settings()

    assert settings.openrouter_api_key == "test-api-key"
    assert settings.openrouter_model == "test-model"


def test_missing_api_key(monkeypatch):

    monkeypatch.delenv(
        "OPENROUTER_API_KEY",
        raising=False
    )

    monkeypatch.setenv(
        "OPENROUTER_MODEL",
        "test-model"
    )

    with pytest.raises(ValueError):
        get_settings()


def test_missing_model(monkeypatch):

    monkeypatch.setenv(
        "OPENROUTER_API_KEY",
        "test-api-key"
    )

    monkeypatch.delenv(
        "OPENROUTER_MODEL",
        raising=False
    )

    with pytest.raises(ValueError):
        get_settings()


def test_validate_settings(monkeypatch):

    monkeypatch.setenv(
        "OPENROUTER_API_KEY",
        "test-api-key"
    )

    monkeypatch.setenv(
        "OPENROUTER_MODEL",
        "test-model"
    )

    assert validate_settings() is True
