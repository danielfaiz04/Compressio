import requests
import os
import time
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "http://localhost:8000"
API_KEY = "demo-key-123" # Use the default key for testing
HEADERS = {"X-API-Key": API_KEY}

def test_endpoint(endpoint: str, method: str, files=None, data=None, expected_status: int = 200):
    url = f"{BASE_URL}{endpoint}"
    logging.info(f"Testing {method} {url}...")
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, files=files, data=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        logging.info(f"Response Status: {response.status_code}, Expected: {expected_status}")
        logging.debug(f"Response Body: {response.text}")

        assert response.status_code == expected_status, \
            f"Expected status {expected_status} for {endpoint}, got {response.status_code}. Response: {response.text}"
        logging.info(f"Test passed for {endpoint}")
        return response.json() if response.content else {}
    except Exception as e:
        logging.error(f"Test failed for {endpoint}: {e}", exc_info=True)
        raise

def create_dummy_file(filename="test_file.txt", content="This is a test file for API key authentication."):
    with open(filename, "w") as f:
        f.write(content)
    return filename

def cleanup_dummy_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def run_all_tests():
    logging.info("\n--- Running API Key Authentication Tests ---")

    dummy_file = create_dummy_file()
    uploaded_file_id = None
    downloaded_file_path = None

    try:
        # Test 1: Health Check (no API key required)
        test_endpoint("/health", "GET")

        # Test 2: Upload with valid API Key
        logging.info("\n--- Test: Upload with valid API Key ---")
        with open(dummy_file, 'rb') as f:
            upload_response = test_endpoint(
                "/upload", "POST", 
                files={'file': (dummy_file, f, 'text/plain')},
                expected_status=202 # Accepted
            )
        uploaded_file_id = upload_response['id']
        logging.info(f"Uploaded file with ID: {uploaded_file_id}")

        # Test 3: Compress with valid API Key
        logging.info("\n--- Test: Compress with valid API Key ---")
        compress_response = test_endpoint(
            "/compress", "POST", 
            data={'file_id': uploaded_file_id, 'method': 'gzip'},
            expected_status=200
        )
        logging.info(f"Compression response: {compress_response}")

        # Test 4: Get result with valid API Key
        logging.info("\n--- Test: Get result with valid API Key ---")
        test_endpoint(f"/result/{uploaded_file_id}", "GET", expected_status=200)

        # Test 5: Download with valid API Key
        logging.info("\n--- Test: Download with valid API Key ---")
        response = requests.get(f"{BASE_URL}/download/{uploaded_file_id}", headers=HEADERS, stream=True)
        response.raise_for_status()
        downloaded_file_path = f"./downloaded_{uploaded_file_id}.gz"
        with open(downloaded_file_path, 'wb') as f_out:
            for chunk in response.iter_content(chunk_size=8192):
                f_out.write(chunk)
        logging.info(f"Downloaded file to {downloaded_file_path}")
        assert os.path.exists(downloaded_file_path)
        logging.info("Test passed for /download")

        # Test 6: Upload with invalid API Key
        logging.info("\n--- Test: Upload with INVALID API Key (expected 401) ---")
        invalid_headers = {"X-API-Key": "invalid-key"}
        with open(dummy_file, 'rb') as f:
            response = requests.post(f"{BASE_URL}/upload", files={'file': (dummy_file, f, 'text/plain')}, headers=invalid_headers)
            assert response.status_code == 401, f"Expected 401, got {response.status_code}. Response: {response.text}"
            logging.info("Test passed: Upload with invalid API Key correctly returned 401.")

        # Test 7: Compress with invalid API Key
        logging.info("\n--- Test: Compress with INVALID API Key (expected 401) ---")
        invalid_headers = {"X-API-Key": "invalid-key"}
        response = requests.post(f"{BASE_URL}/compress", data={'file_id': uploaded_file_id, 'method': 'gzip'}, headers=invalid_headers)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}. Response: {response.text}"
        logging.info("Test passed: Compress with invalid API Key correctly returned 401.")

        # Test 8: Get result with no API Key (expected 401)
        logging.info("\n--- Test: Get result with NO API Key (expected 401) ---")
        response = requests.get(f"{BASE_URL}/result/{uploaded_file_id}") # No headers
        assert response.status_code == 401, f"Expected 401, got {response.status_code}. Response: {response.text}"
        logging.info("Test passed: Get result with no API Key correctly returned 401.")

        logging.info("\nAll API Key authentication tests finished successfully!")

    except Exception as e:
        logging.critical(f"An error occurred during testing: {e}", exc_info=True)
        logging.error("Some tests failed. Please check the backend server and API key configuration.")
    finally:
        cleanup_dummy_file(dummy_file)
        if downloaded_file_path and os.path.exists(downloaded_file_path):
            os.remove(downloaded_file_path)
        # Clean up any files in tmp/uploads and tmp/downloads if left over
        # This requires importing cleanup_old_files or manually deleting
        # For now, rely on periodic cleanup or manual deletion of tmp/*

if __name__ == "__main__":
    run_all_tests() 