"""
Script to train machine learning model and evaluate performance on data slices.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import os

# Import the necessary functions from the starter code
from ml.data import process_data
from ml.model import (
    train_model,
    compute_model_metrics,
    inference,
    save_model,
    save_encoder
)


def main():
    """Main function to train and evaluate the model."""
    
    # Load the data
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "census.csv")
    data = pd.read_csv(data_path)
    
    # Split the data into train and test sets
    train, test = train_test_split(data, test_size=0.20, random_state=42)
    
    # Define categorical features
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
    
    # Process the training data
    X_train, y_train, encoder, lb = process_data(
        train, categorical_features=cat_features, label="salary", training=True
    )
    
    # Process the test data with the trained encoder and label binarizer
    X_test, y_test, _, _ = process_data(
        test, 
        categorical_features=cat_features, 
        label="salary", 
        training=False,
        encoder=encoder,
        lb=lb
    )
    
    # Train the model
    print("Training model...")
    model = train_model(X_train, y_train)
    
    # Evaluate on test set
    print("Evaluating model on test set...")
    preds = inference(model, X_test)
    precision, recall, fbeta = compute_model_metrics(y_test, preds)
    
    print("Overall Model Performance:")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall: {recall:.4f}")
    print(f"  F1 Score: {fbeta:.4f}")
    
    # Save the model and encoders
    model_dir = os.path.join(os.path.dirname(__file__), "..", "model")
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, "model.pkl")
    encoder_path = os.path.join(model_dir, "encoder.pkl")
    lb_path = os.path.join(model_dir, "lb.pkl")
    
    print("Saving model and encoders...")
    save_model(model, model_path)
    save_encoder(encoder, encoder_path)
    save_encoder(lb, lb_path)
    
    # Compute performance on slices of data
    print("\nComputing performance on data slices...")
    output_file = os.path.join(os.path.dirname(__file__), "..", "slice_output.txt")
    
    with open(output_file, 'w') as f:
        f.write("Model Performance on Data Slices\n")
        f.write("=" * 80 + "\n\n")
        
        # Compute slices for each categorical feature
        for feature in cat_features:
            f.write(f"\nSlice Performance for Feature: {feature}\n")
            f.write("-" * 80 + "\n")
            
            unique_values = test[feature].unique()
            
            for value in sorted(unique_values):
                # Get slice of test data
                slice_mask = test[feature] == value
                test_slice = test[slice_mask].copy()
                
                if len(test_slice) == 0:
                    continue
                
                # Process the slice
                X_slice, y_slice, _, _ = process_data(
                    test_slice,
                    categorical_features=cat_features,
                    label="salary",
                    training=False,
                    encoder=encoder,
                    lb=lb
                )
                
                # Make predictions
                preds_slice = inference(model, X_slice)
                
                # Compute metrics
                precision_slice, recall_slice, fbeta_slice = compute_model_metrics(
                    y_slice, preds_slice
                )
                
                f.write(f"  {feature}={value}\n")
                f.write(f"    Samples: {len(test_slice)}\n")
                f.write(f"    Precision: {precision_slice:.4f}\n")
                f.write(f"    Recall: {recall_slice:.4f}\n")
                f.write(f"    F1 Score: {fbeta_slice:.4f}\n")
                f.write("\n")
    
    print(f"Slice performance saved to {output_file}")
    print("Training complete!")


if __name__ == "__main__":
    main()
