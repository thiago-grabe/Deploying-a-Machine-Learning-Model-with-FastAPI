"""
FastAPI application for Census Income Classification Model.
"""

import os
import sys

# Add the starter directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'starter'))

from fastapi import FastAPI  # noqa: E402
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

# Load model and encoders at startup
model_dir = os.path.join(os.path.dirname(__file__), "model")
model = load_model(os.path.join(model_dir, "model.pkl"))
encoder = load_encoder(os.path.join(model_dir, "encoder.pkl"))
lb = load_encoder(os.path.join(model_dir, "lb.pkl"))

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


class CensusData(BaseModel):
    """
    Pydantic model for input data validation.
    Uses Field with alias to handle column names with hyphens.
    """
    model_config = {"populate_by_name": True}
    
    age: int = Field(..., json_schema_extra={"example": 37})
    workclass: str = Field(..., json_schema_extra={"example": "Private"})
    fnlgt: int = Field(..., json_schema_extra={"example": 178356})
    education: str = Field(..., json_schema_extra={"example": "HS-grad"})
    education_num: int = Field(..., alias="education-num", json_schema_extra={"example": 10})
    marital_status: str = Field(..., alias="marital-status", json_schema_extra={"example": "Married-civ-spouse"})
    occupation: str = Field(..., json_schema_extra={"example": "Prof-specialty"})
    relationship: str = Field(..., json_schema_extra={"example": "Husband"})
    race: str = Field(..., json_schema_extra={"example": "White"})
    sex: str = Field(..., json_schema_extra={"example": "Male"})
    capital_gain: int = Field(..., alias="capital-gain", json_schema_extra={"example": 0})
    capital_loss: int = Field(..., alias="capital-loss", json_schema_extra={"example": 0})
    hours_per_week: int = Field(..., alias="hours-per-week", json_schema_extra={"example": 40})
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


@app.post("/predict", response_model=PredictionResponse)
async def predict(data: CensusData):
    """
    Perform model inference on provided census data.
    
    Args:
        data: Census data features
        
    Returns:
        PredictionResponse: Prediction result
    """
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
    
    return PredictionResponse(prediction=prediction_label)
