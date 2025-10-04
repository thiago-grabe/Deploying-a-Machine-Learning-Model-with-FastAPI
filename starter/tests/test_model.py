"""
Unit tests for the ML model functions.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter'))

import pytest
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, LabelBinarizer
import tempfile

from ml.model import (
    train_model,
    compute_model_metrics,
    inference,
    save_model,
    load_model,
    save_encoder,
    load_encoder
)
from ml.data import process_data


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    data = pd.DataFrame({
        'age': [39, 50, 38, 53, 28],
        'workclass': ['State-gov', 'Self-emp-not-inc', 'Private', 'Private', 'Private'],
        'education': ['Bachelors', 'Bachelors', 'HS-grad', '11th', 'Bachelors'],
        'education-num': [13, 13, 9, 7, 13],
        'marital-status': ['Never-married', 'Married-civ-spouse', 'Divorced', 
                          'Married-civ-spouse', 'Married-civ-spouse'],
        'occupation': ['Adm-clerical', 'Exec-managerial', 'Handlers-cleaners',
                      'Handlers-cleaners', 'Prof-specialty'],
        'relationship': ['Not-in-family', 'Husband', 'Not-in-family', 'Husband', 'Wife'],
        'race': ['White', 'White', 'White', 'Black', 'Black'],
        'sex': ['Male', 'Male', 'Male', 'Male', 'Female'],
        'capital-gain': [2174, 0, 0, 0, 0],
        'capital-loss': [0, 0, 0, 0, 0],
        'hours-per-week': [40, 13, 40, 40, 40],
        'native-country': ['United-States', 'United-States', 'United-States',
                          'United-States', 'Cuba'],
        'salary': ['<=50K', '<=50K', '<=50K', '<=50K', '<=50K']
    })
    return data


@pytest.fixture
def processed_data(sample_data):
    """Process sample data for testing."""
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
    
    X, y, encoder, lb = process_data(
        sample_data,
        categorical_features=cat_features,
        label="salary",
        training=True
    )
    
    return X, y, encoder, lb


def test_train_model_returns_correct_type(processed_data):
    """Test that train_model returns a RandomForestClassifier."""
    X, y, _, _ = processed_data
    model = train_model(X, y)
    
    assert isinstance(model, RandomForestClassifier), \
        "train_model should return a RandomForestClassifier"
    assert hasattr(model, 'predict'), \
        "Model should have a predict method"


def test_train_model_can_fit(processed_data):
    """Test that the trained model can make predictions."""
    X, y, _, _ = processed_data
    model = train_model(X, y)
    
    # Model should be fitted
    assert hasattr(model, 'classes_'), \
        "Model should be fitted and have classes_ attribute"
    
    # Should be able to make predictions
    predictions = model.predict(X)
    assert len(predictions) == len(y), \
        "Number of predictions should match number of samples"


def test_inference_returns_correct_shape(processed_data):
    """Test that inference returns predictions with correct shape."""
    X, y, _, _ = processed_data
    model = train_model(X, y)
    
    preds = inference(model, X)
    
    assert isinstance(preds, np.ndarray), \
        "Inference should return a numpy array"
    assert preds.shape[0] == X.shape[0], \
        "Number of predictions should match number of samples"
    assert len(preds.shape) == 1, \
        "Predictions should be 1-dimensional"


def test_compute_model_metrics_returns_correct_types(processed_data):
    """Test that compute_model_metrics returns three float values."""
    X, y, _, _ = processed_data
    model = train_model(X, y)
    preds = inference(model, X)
    
    precision, recall, fbeta = compute_model_metrics(y, preds)
    
    assert isinstance(precision, (float, np.floating)), \
        "Precision should be a float"
    assert isinstance(recall, (float, np.floating)), \
        "Recall should be a float"
    assert isinstance(fbeta, (float, np.floating)), \
        "F-beta should be a float"


def test_compute_model_metrics_values_in_valid_range(processed_data):
    """Test that metrics are in the valid range [0, 1]."""
    X, y, _, _ = processed_data
    model = train_model(X, y)
    preds = inference(model, X)
    
    precision, recall, fbeta = compute_model_metrics(y, preds)
    
    assert 0 <= precision <= 1, "Precision should be between 0 and 1"
    assert 0 <= recall <= 1, "Recall should be between 0 and 1"
    assert 0 <= fbeta <= 1, "F-beta should be between 0 and 1"


def test_save_and_load_model(processed_data):
    """Test that models can be saved and loaded correctly."""
    X, y, _, _ = processed_data
    model = train_model(X, y)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
        temp_path = f.name
    
    try:
        # Save and load the model
        save_model(model, temp_path)
        loaded_model = load_model(temp_path)
        
        # Check that loaded model works
        assert isinstance(loaded_model, RandomForestClassifier), \
            "Loaded model should be a RandomForestClassifier"
        
        # Predictions should be the same
        original_preds = model.predict(X)
        loaded_preds = loaded_model.predict(X)
        
        np.testing.assert_array_equal(original_preds, loaded_preds,
                                     "Loaded model predictions should match original")
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_save_and_load_encoder(processed_data):
    """Test that encoders can be saved and loaded correctly."""
    _, _, encoder, _ = processed_data
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
        temp_path = f.name
    
    try:
        # Save and load the encoder
        save_encoder(encoder, temp_path)
        loaded_encoder = load_encoder(temp_path)
        
        # Check that loaded encoder works
        assert isinstance(loaded_encoder, OneHotEncoder), \
            "Loaded encoder should be a OneHotEncoder"
        
        # Should have the same categories
        assert len(loaded_encoder.categories_) == len(encoder.categories_), \
            "Loaded encoder should have same number of categories"
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_process_data_training_mode(sample_data):
    """Test process_data in training mode."""
    cat_features = ["workclass", "education"]
    
    X, y, encoder, lb = process_data(
        sample_data,
        categorical_features=cat_features,
        label="salary",
        training=True
    )
    
    assert isinstance(X, np.ndarray), "X should be a numpy array"
    assert isinstance(y, np.ndarray), "y should be a numpy array"
    assert isinstance(encoder, OneHotEncoder), "encoder should be a OneHotEncoder"
    assert isinstance(lb, LabelBinarizer), "lb should be a LabelBinarizer"
    assert X.shape[0] == len(sample_data), "Number of samples should be preserved"


def test_process_data_inference_mode(sample_data):
    """Test process_data in inference mode."""
    cat_features = ["workclass", "education"]
    
    # First, get encoders from training mode
    X_train, y_train, encoder, lb = process_data(
        sample_data,
        categorical_features=cat_features,
        label="salary",
        training=True
    )
    
    # Now use them in inference mode
    X_test, y_test, _, _ = process_data(
        sample_data,
        categorical_features=cat_features,
        label="salary",
        training=False,
        encoder=encoder,
        lb=lb
    )
    
    assert isinstance(X_test, np.ndarray), "X_test should be a numpy array"
    assert isinstance(y_test, np.ndarray), "y_test should be a numpy array"
    assert X_test.shape[1] == X_train.shape[1], \
        "Feature dimensions should match between train and test"

