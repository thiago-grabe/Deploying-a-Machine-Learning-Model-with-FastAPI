"""
Unit tests for the FastAPI application.
"""

from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app

# Create test client
client = TestClient(app)


def test_get_root():
    """
    Test GET on root path.
    Tests both status code and response content.
    """
    response = client.get("/")
    
    # Test status code
    assert response.status_code == 200, \
        f"Expected status code 200, got {response.status_code}"
    
    # Test response content
    response_json = response.json()
    assert "message" in response_json, \
        "Response should contain 'message' field"
    assert isinstance(response_json["message"], str), \
        "Message should be a string"
    assert len(response_json["message"]) > 0, \
        "Message should not be empty"


def test_post_predict_low_income():
    """
    Test POST for prediction of low income (<=50K).
    This tests one possible inference result.
    """
    # Sample data that should predict <=50K
    input_data = {
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
    
    response = client.post("/predict", json=input_data)
    
    # Test status code
    assert response.status_code == 200, \
        f"Expected status code 200, got {response.status_code}"
    
    # Test response content
    response_json = response.json()
    assert "prediction" in response_json, \
        "Response should contain 'prediction' field"
    assert response_json["prediction"] in ["<=50K", ">50K"], \
        "Prediction should be either '<=50K' or '>50K'"


def test_post_predict_high_income():
    """
    Test POST for prediction of high income (>50K).
    This tests the other possible inference result.
    """
    # Sample data that should predict >50K
    input_data = {
        "age": 52,
        "workclass": "Self-emp-inc",
        "fnlgt": 287927,
        "education": "HS-grad",
        "education-num": 9,
        "marital-status": "Married-civ-spouse",
        "occupation": "Exec-managerial",
        "relationship": "Wife",
        "race": "White",
        "sex": "Female",
        "capital-gain": 15024,
        "capital-loss": 0,
        "hours-per-week": 40,
        "native-country": "United-States"
    }
    
    response = client.post("/predict", json=input_data)
    
    # Test status code
    assert response.status_code == 200, \
        f"Expected status code 200, got {response.status_code}"
    
    # Test response content
    response_json = response.json()
    assert "prediction" in response_json, \
        "Response should contain 'prediction' field"
    assert response_json["prediction"] in ["<=50K", ">50K"], \
        "Prediction should be either '<=50K' or '>50K'"


def test_post_predict_validation():
    """
    Test that POST validates input data correctly.
    """
    # Missing required field
    invalid_data = {
        "age": 30,
        "workclass": "Private"
        # Missing other required fields
    }
    
    response = client.post("/predict", json=invalid_data)
    
    # Should return 422 for validation error
    assert response.status_code == 422, \
        "Should return 422 for invalid input"


def test_get_openapi_docs():
    """
    Test that OpenAPI documentation is available.
    """
    response = client.get("/openapi.json")
    
    assert response.status_code == 200, \
        "OpenAPI docs should be accessible"
    
    openapi_json = response.json()
    assert "openapi" in openapi_json, \
        "Response should be valid OpenAPI schema"

