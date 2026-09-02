"""
Tests for deployment-related additions: /health endpoint, input validation
bounds, unknown-category warning logging, and the Vercel entrypoint shim.
"""

import logging
import sys
import os
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
# Repo root APPENDED (not inserted) so it can never shadow starter/ modules;
# needed to import the root Vercel shim app.py from tests run inside starter/.
sys.path.append(str(Path(__file__).resolve().parents[2]))

from main import app

client = TestClient(app)


def valid_payload(**overrides):
    """Return a known-valid /predict payload, optionally overridden."""
    payload = {
        "age": 25,
        "workclass": "Private",
        "fnlgt": 226802,
        "education": "11th",
        "education-num": 7,
        "marital-status": "Never-married",
        "occupation": "Machine-op-inspct",
        "relationship": "Own-child",
        "race": "Black",
        "sex": "Male",
        "capital-gain": 0,
        "capital-loss": 0,
        "hours-per-week": 40,
        "native-country": "United-States"
    }
    payload.update(overrides)
    return payload


def test_vercel_shim_exports_same_app():
    """The root app.py Vercel shim must re-export the exact same FastAPI
    instance that starter/main.py defines (identity, not a copy)."""
    import app as vercel_shim
    import main

    assert vercel_shim.app is main.app


def test_health():
    """GET /health returns service status and model metadata."""
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True
    assert "sklearn_version" in body
    assert "model_type" in body


def test_ui_page_served():
    """GET /ui returns the web UI HTML."""
    response = client.get("/ui")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Census Income Classifier" in response.text


def test_predict_rejects_negative_age():
    """Out-of-bounds numeric input must fail validation with 422."""
    response = client.post("/predict", json=valid_payload(age=-5))

    assert response.status_code == 422


def test_unknown_category_logs_warning(caplog):
    """A category outside the training vocabulary still predicts (the encoder
    zero-encodes it) but must emit a WARNING naming the feature."""
    with caplog.at_level(logging.WARNING):
        response = client.post("/predict", json=valid_payload(workclass="Klingon"))

    assert response.status_code == 200
    assert response.json()["prediction"] in ["<=50K", ">50K"]
    warnings = [r for r in caplog.records if r.levelno >= logging.WARNING]
    assert any("workclass" in r.getMessage() for r in warnings), \
        "Expected a WARNING mentioning the unknown 'workclass' value"
