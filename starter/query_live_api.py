"""
Script to query the live API deployed on a cloud platform.
Usage: python query_live_api.py [API_URL]

If no URL is provided, it will use the default localhost URL for testing.
"""

import json
import logging
import os
import sys
import time

import requests

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 30  # seconds; requests hangs forever without one


def query_api(base_url):
    """
    Query the live API with sample data.
    
    Args:
        base_url: Base URL of the deployed API
    """
    logger.info("Querying API at %s", base_url)
    print(f"Querying API at: {base_url}")
    print("=" * 80)

    # Test 1: GET request on root
    print("\n1. Testing GET request on root endpoint...")
    try:
        start = time.perf_counter()
        response = requests.get(f"{base_url}/", timeout=REQUEST_TIMEOUT)
        logger.info(
            "GET / status=%d elapsed_ms=%.1f",
            response.status_code, (time.perf_counter() - start) * 1000
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        logger.error("GET / failed: %s", e)
        print(f"Error: {e}")
        return
    
    # Test 2: POST request - Example predicting <=50K
    print("\n2. Testing POST request - Low income example...")
    low_income_data = {
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
    
    try:
        start = time.perf_counter()
        response = requests.post(
            f"{base_url}/predict",
            json=low_income_data,
            timeout=REQUEST_TIMEOUT
        )
        logger.info(
            "POST /predict (low income) status=%d elapsed_ms=%.1f",
            response.status_code, (time.perf_counter() - start) * 1000
        )
        print(f"Status Code: {response.status_code}")
        print(f"Input Data: {json.dumps(low_income_data, indent=2)}")
        print(f"Prediction: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        logger.error("POST /predict (low income) failed: %s", e)
        print(f"Error: {e}")
    
    # Test 3: POST request - Example predicting >50K
    print("\n3. Testing POST request - High income example...")
    high_income_data = {
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
    
    try:
        start = time.perf_counter()
        response = requests.post(
            f"{base_url}/predict",
            json=high_income_data,
            timeout=REQUEST_TIMEOUT
        )
        logger.info(
            "POST /predict (high income) status=%d elapsed_ms=%.1f",
            response.status_code, (time.perf_counter() - start) * 1000
        )
        print(f"Status Code: {response.status_code}")
        print(f"Input Data: {json.dumps(high_income_data, indent=2)}")
        print(f"Prediction: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        logger.error("POST /predict (high income) failed: %s", e)
        print(f"Error: {e}")
    
    print("\n" + "=" * 80)
    print("API query completed!")


def main():
    """Main function to run the API query script."""
    
    # Check if URL is provided as command line argument
    if len(sys.argv) > 1:
        api_url = sys.argv[1].rstrip('/')
    else:
        # Default to localhost for testing
        api_url = "http://localhost:8000"
        print("No URL provided. Using default localhost URL.")
        print("Usage: python query_live_api.py [API_URL]")
        print("Example: python query_live_api.py https://your-app.herokuapp.com")
    
    query_api(api_url)


if __name__ == "__main__":
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    main()

