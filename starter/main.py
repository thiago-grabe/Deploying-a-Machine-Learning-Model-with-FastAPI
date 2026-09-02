"""
FastAPI application for Census Income Classification Model.
"""

import logging
import os
import sys
import time
import uuid

# Add the starter directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'starter'))

# Configure logging once, at the serverless entrypoint. stream=sys.stdout is
# required on Vercel: stderr lines are classified as errors, and an
# unconfigured root logger drops INFO entirely.
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stdout,
)
logging.captureWarnings(True)
logger = logging.getLogger(__name__)

import numpy as np  # noqa: E402
import sklearn  # noqa: E402
from fastapi import FastAPI, HTTPException, Request  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402
import pandas as pd  # noqa: E402

from ml.model import inference, load_model, load_encoder  # noqa: E402
from ml.data import process_data  # noqa: E402

# Initialize FastAPI app
app = FastAPI(
    title="Census Income Classification API",
    description="Predict whether income exceeds $50K/yr based on census data",
    version="1.0.0"
)

# Load model and encoders at startup. Failures log and re-raise: on serverless
# a crashed cold start is one obvious ERROR, not a half-alive app.
_cold_start = time.perf_counter()
model_dir = os.path.join(os.path.dirname(__file__), "model")
model = load_model(os.path.join(model_dir, "model.pkl"))
encoder = load_encoder(os.path.join(model_dir, "encoder.pkl"))
lb = load_encoder(os.path.join(model_dir, "lb.pkl"))

logger.info(
    "Cold start complete in %.1fms: python=%s sklearn=%s numpy=%s model=%s "
    "n_estimators=%s n_features_in=%s",
    (time.perf_counter() - _cold_start) * 1000,
    sys.version.split()[0],
    sklearn.__version__,
    np.__version__,
    type(model).__name__,
    getattr(model, "n_estimators", "?"),
    getattr(model, "n_features_in_", "?"),
)

# Categorical features for processing
cat_features = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",
]


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every request: method, path, status, latency, request id."""
    rid = request.headers.get("x-vercel-id") or uuid.uuid4().hex[:8]
    request.state.rid = rid
    start = time.perf_counter()
    response = await call_next(request)
    logger.info(
        "%s %s status=%d elapsed_ms=%.1f rid=%s",
        request.method, request.url.path, response.status_code,
        (time.perf_counter() - start) * 1000, rid,
    )
    return response


class CensusData(BaseModel):
    """
    Pydantic model for input data validation.
    Uses Field with alias to handle column names with hyphens.
    """
    model_config = {"populate_by_name": True}

    age: int = Field(..., gt=0, le=120, json_schema_extra={"example": 37})
    workclass: str = Field(..., json_schema_extra={"example": "Private"})
    fnlgt: int = Field(..., gt=0, json_schema_extra={"example": 178356})
    education: str = Field(..., json_schema_extra={"example": "HS-grad"})
    education_num: int = Field(..., alias="education-num", ge=1, le=16, json_schema_extra={"example": 9})
    marital_status: str = Field(..., alias="marital-status", json_schema_extra={"example": "Married-civ-spouse"})
    occupation: str = Field(..., json_schema_extra={"example": "Prof-specialty"})
    relationship: str = Field(..., json_schema_extra={"example": "Husband"})
    race: str = Field(..., json_schema_extra={"example": "White"})
    sex: str = Field(..., json_schema_extra={"example": "Male"})
    capital_gain: int = Field(..., alias="capital-gain", ge=0, json_schema_extra={"example": 0})
    capital_loss: int = Field(..., alias="capital-loss", ge=0, json_schema_extra={"example": 0})
    hours_per_week: int = Field(..., alias="hours-per-week", ge=1, le=168, json_schema_extra={"example": 40})
    native_country: str = Field(..., alias="native-country", json_schema_extra={"example": "United-States"})


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    prediction: str = Field(..., description="Predicted salary class: '>50K' or '<=50K'")


@app.get("/")
async def welcome():
    """
    Welcome endpoint for the API.

    Returns:
        dict: Welcome message
    """
    return {
        "message": "Welcome to the Census Income Classification API!",
        "docs": "Visit /docs for API documentation",
        "health": "operational"
    }


@app.get("/health")
async def health():
    """
    Health endpoint for uptime monitors and deployment smoke tests.

    Returns:
        dict: Service health and model metadata
    """
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_type": type(model).__name__,
        "sklearn_version": sklearn.__version__,
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(data: CensusData, request: Request):
    """
    Perform model inference on provided census data.

    Args:
        data: Census data features
        request: Incoming request (used for request-id correlation)

    Returns:
        PredictionResponse: Prediction result
    """
    rid = getattr(request.state, "rid", "-")
    start = time.perf_counter()

    # Convert input data to DataFrame with correct column names
    input_dict = {
        'age': data.age,
        'workclass': data.workclass,
        'fnlgt': data.fnlgt,
        'education': data.education,
        'education-num': data.education_num,
        'marital-status': data.marital_status,
        'occupation': data.occupation,
        'relationship': data.relationship,
        'race': data.race,
        'sex': data.sex,
        'capital-gain': data.capital_gain,
        'capital-loss': data.capital_loss,
        'hours-per-week': data.hours_per_week,
        'native-country': data.native_country
    }
    # Census features are demographic/protected attributes: full inputs are
    # DEBUG-only; INFO carries the label and latency, never feature values.
    logger.debug("predict input rid=%s: %s", rid, input_dict)

    try:
        input_df = pd.DataFrame([input_dict])

        # Process the data
        X, _, _, _ = process_data(
            input_df,
            categorical_features=cat_features,
            label=None,
            training=False,
            encoder=encoder,
            lb=lb
        )

        # Make prediction
        pred = inference(model, X)

        # Convert prediction back to label
        prediction_label = lb.inverse_transform(pred)[0]
    except Exception:
        logger.exception("predict failed rid=%s", rid)
        raise HTTPException(status_code=500, detail="Internal error during inference")

    logger.info(
        "predict prediction=%s elapsed_ms=%.1f rid=%s",
        prediction_label, (time.perf_counter() - start) * 1000, rid,
    )
    return PredictionResponse(prediction=prediction_label)
