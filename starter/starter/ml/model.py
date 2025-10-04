from sklearn.metrics import fbeta_score, precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
import pickle
import os


def train_model(X_train, y_train):
    """
    Trains a machine learning model and returns it.

    Inputs
    ------
    X_train : np.ndarray
        Training data.
    y_train : np.ndarray
        Labels.
    Returns
    -------
    model : RandomForestClassifier
        Trained machine learning model.
    """
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model


def compute_model_metrics(y, preds):
    """
    Validates the trained machine learning model using precision, recall, and F1.

    Inputs
    ------
    y : np.ndarray
        Known labels, binarized.
    preds : np.ndarray
        Predicted labels, binarized.
    Returns
    -------
    precision : float
    recall : float
    fbeta : float
    """
    fbeta = fbeta_score(y, preds, beta=1, zero_division=1)
    precision = precision_score(y, preds, zero_division=1)
    recall = recall_score(y, preds, zero_division=1)
    return precision, recall, fbeta


def inference(model, X):
    """ Run model inferences and return the predictions.

    Inputs
    ------
    model : RandomForestClassifier
        Trained machine learning model.
    X : np.ndarray
        Data used for prediction.
    Returns
    -------
    preds : np.ndarray
        Predictions from the model.
    """
    preds = model.predict(X)
    return preds


def save_model(model, path):
    """
    Save a trained model to disk.

    Inputs
    ------
    model : RandomForestClassifier
        Trained machine learning model.
    path : str
        Path to save the model.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(model, f)


def load_model(path):
    """
    Load a trained model from disk.

    Inputs
    ------
    path : str
        Path to the saved model.
    
    Returns
    -------
    model : RandomForestClassifier
        Loaded machine learning model.
    """
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


def save_encoder(encoder, path):
    """
    Save an encoder to disk.

    Inputs
    ------
    encoder : OneHotEncoder or LabelBinarizer
        Trained encoder.
    path : str
        Path to save the encoder.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(encoder, f)


def load_encoder(path):
    """
    Load an encoder from disk.

    Inputs
    ------
    path : str
        Path to the saved encoder.
    
    Returns
    -------
    encoder : OneHotEncoder or LabelBinarizer
        Loaded encoder.
    """
    with open(path, 'rb') as f:
        encoder = pickle.load(f)
    return encoder


def compute_model_metrics_on_slices(model, X, y, feature_slice, categorical_features, encoder):
    """
    Compute model metrics on data slices.

    Inputs
    ------
    model : RandomForestClassifier
        Trained machine learning model.
    X : pd.DataFrame
        Feature data.
    y : pd.Series
        Labels.
    feature_slice : str
        Name of the categorical feature to slice on.
    categorical_features : list
        List of categorical feature names.
    encoder : OneHotEncoder
        Trained encoder.
    
    Returns
    -------
    slice_metrics : dict
        Dictionary containing metrics for each slice.
    """
    from .data import process_data
    
    slice_metrics = {}
    unique_values = X[feature_slice].unique()
    
    for value in unique_values:
        # Get slice of data
        slice_idx = X[feature_slice] == value
        X_slice = X[slice_idx]
        y_slice = y[slice_idx]
        
        if len(X_slice) == 0:
            continue
        
        # Process the slice
        X_processed, y_processed, _, _ = process_data(
            X_slice.copy(),
            categorical_features=categorical_features,
            label=None,
            training=False,
            encoder=encoder,
            lb=None
        )
        
        # Make predictions
        preds = inference(model, X_processed)
        
        # Compute metrics
        precision, recall, fbeta = compute_model_metrics(y_slice.values, preds)
        
        slice_metrics[value] = {
            'precision': precision,
            'recall': recall,
            'fbeta': fbeta,
            'n_samples': len(X_slice)
        }
    
    return slice_metrics
