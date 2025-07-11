import requests
from typing import Dict, Any, List, Optional
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SmartShrinkClient:
    def __init__(self, base_url: str, api_key: str = "demo-key-123"):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "X-API-Key": self.api_key
        }

    def _send_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error for {endpoint}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text) from e
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection Error for {endpoint}: {e}")
            raise HTTPException(status_code=503, detail=f"Could not connect to the SmartShrink backend: {e}") from e
        except requests.exceptions.Timeout as e:
            logging.error(f"Timeout Error for {endpoint}: {e}")
            raise HTTPException(status_code=504, detail=f"Request to SmartShrink backend timed out: {e}") from e
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Error for {endpoint}: {e}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}") from e

    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        Uploads a file to the backend.
        Returns metadata of the uploaded file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(file_path, "rb") as f:
            files = {'file': (os.path.basename(file_path), f)}
            logging.info(f"Uploading file: {file_path}")
            return self._send_request("POST", "/upload", files=files)

    def compress_file(self, file_id: str, method: str, profile: Optional[str] = None, sensitive_mode: bool = False) -> Dict[str, Any]:
        """
        Compresses an uploaded file.
        Returns compression results.
        """
        data = {'file_id': file_id, 'method': method}
        if profile: data['profile'] = profile
        data['sensitive_mode'] = sensitive_mode
        logging.info(f"Compressing file ID {file_id} with method {method}, profile {profile}, sensitive_mode {sensitive_mode}")
        return self._send_request("POST", "/compress", data=data)

    def get_compression_result(self, file_id: str) -> Dict[str, Any]:
        """
        Gets compression result metadata for a file ID.
        """
        logging.info(f"Fetching compression result for file ID: {file_id}")
        return self._send_request("GET", f"/result/{file_id}")

    def download_file(self, file_id: str, download_path: str, original: bool = False) -> str:
        """
        Downloads a compressed or original file.
        Returns the path to the downloaded file.
        """
        endpoint = f"/download/{file_id}"
        params = {'original': original}
        logging.info(f"Downloading file ID: {file_id}, original: {original}")
        
        url = f"{self.base_url}{endpoint}"
        try:
            with requests.get(url, headers=self.headers, params=params, stream=True) as response:
                response.raise_for_status()
                # Extract filename from Content-Disposition header if available
                cd = response.headers.get('Content-Disposition')
                if cd:
                    # Example: attachment; filename="compressed_abc123_example.pdf"
                    filename = cd.split('filename=')[-1].strip('\" ')
                else:
                    filename = f"downloaded_{file_id}"
                
                full_download_path = os.path.join(download_path, filename)
                os.makedirs(download_path, exist_ok=True)

                with open(full_download_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logging.info(f"File downloaded to: {full_download_path}")
                return full_download_path
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error downloading {endpoint}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text) from e
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Error downloading {endpoint}: {e}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred during download: {e}") from e

    def compare_files(self, file_id: str) -> Dict[str, Any]:
        """
        Gets comparison statistics, ratio, previews, and diff summary for a file.
        """
        logging.info(f"Fetching comparison for file ID: {file_id}")
        return self._send_request("GET", f"/compare/{file_id}")

    def batch_compress(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compresses multiple files in a batch.
        items: List of dictionaries, each with 'file_id', 'method', optional 'profile', 'sensitive_mode'.
        """
        logging.info(f"Initiating batch compression for {len(items)} items.")
        # FastAPI expects form data for batch_compress, so we need to encode the list as JSON string
        # and send it as a form field or modify the FastAPI endpoint to accept JSON body.
        # Assuming FastAPI endpoint expects 'items' as a JSON string within form-data for simplicity here.
        # If the backend expects application/json, change `data` to `json`.
        data = {"items": json.dumps(items)}
        return self._send_request("POST", "/batch_compress", data=data)

    def diff_compress(self, file_id: str, method: str, base_file_id: Optional[str] = None, patch_file_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Creates or applies a differential compression patch.
        method: 'patch' or 'restore'
        """
        data = {"file_id": file_id, "method": method}
        if base_file_id: data['base_file_id'] = base_file_id
        if patch_file_id: data['patch_file_id'] = patch_file_id
        logging.info(f"Performing differential compression: method={method}, file_id={file_id}, base_file_id={base_file_id}, patch_file_id={patch_file_id}")
        return self._send_request("POST", "/diff_compress", data=data)

    def get_compression_methods(self) -> Dict[str, Any]:
        """
        Lists available compression methods.
        """
        logging.info("Fetching available compression methods.")
        return self._send_request("GET", "/compression_methods")

if __name__ == "__main__":
    # Example Usage
    BASE_URL = "http://localhost:8000"
    client = SmartShrinkClient(BASE_URL, api_key="demo-key-123")
    
    # --- Health Check ---
    try:
        health = client._send_request("GET", "/health") # Using internal method for health check
        print(f"Health Check: {health}")
    except Exception as e:
        print(f"Health check failed: {e}")
        print("Please ensure the backend server is running (e.g., uvicorn backend.main:app --reload)")
        exit()

    # --- Upload File ---
    # Create a dummy file for upload
    dummy_file_path = "dummy.txt"
    with open(dummy_file_path, "w") as f:
        f.write("This is a dummy text file for testing compression.\n")
        f.write("It has multiple lines to see if compression works effectively.\n")
        f.write("Hello World! This is a test. 12345.\n")

    uploaded_file_id = None
    try:
        print(f"\n--- Uploading {dummy_file_path} ---")
        upload_result = client.upload_file(dummy_file_path)
        uploaded_file_id = upload_result['id']
        print(f"Upload successful: {upload_result}")

        # --- Compress File (e.g., gzip) ---
        print(f"\n--- Compressing file {uploaded_file_id} with gzip ---")
        compress_result = client.compress_file(uploaded_file_id, method="gzip")
        print(f"Compression successful: {compress_result}")

        # --- Get Result Metadata ---
        print(f"\n--- Getting result metadata for {uploaded_file_id} ---")
        result_meta = client.get_compression_result(uploaded_file_id)
        print(f"Result metadata: {result_meta}")

        # --- Download Compressed File ---
        download_dir = "./downloads_test"
        os.makedirs(download_dir, exist_ok=True)
        print(f"\n--- Downloading compressed file {uploaded_file_id} to {download_dir} ---")
        downloaded_path = client.download_file(uploaded_file_id, download_dir)
        print(f"File downloaded to: {downloaded_path}")
        
        # --- Download Original File ---
        print(f"\n--- Downloading original file {uploaded_file_id} to {download_dir} ---")
        downloaded_original_path = client.download_file(uploaded_file_id, download_dir, original=True)
        print(f"Original file downloaded to: {downloaded_original_path}")

        # --- Compare Files ---
        print(f"\n--- Comparing file {uploaded_file_id} ---")
        compare_results = client.compare_files(uploaded_file_id)
        print(f"Comparison Results: {compare_results}")

        # --- Batch Compress Example ---
        # Upload a second dummy file
        dummy_file_path_2 = "dummy2.txt"
        with open(dummy_file_path_2, "w") as f:
            f.write("This is another dummy file.\nIt will be part of a batch compression.\n")
        upload_result_2 = client.upload_file(dummy_file_path_2)
        uploaded_file_id_2 = upload_result_2['id']

        batch_items = [
            {"file_id": uploaded_file_id, "method": "brotli"},
            {"file_id": uploaded_file_id_2, "method": "gzip"}
        ]
        print(f"\n--- Running Batch Compression ---")
        batch_results = client.batch_compress(batch_items)
        print(f"Batch Compression Results: {batch_results}")

        # --- Diff Compress Example (requires two uploaded files) ---
        # Assume uploaded_file_id is version 1, uploaded_file_id_2 is version 2
        print(f"\n--- Creating Diff Patch from {uploaded_file_id} to {uploaded_file_id_2} ---")
        try:
            diff_patch_result = client.diff_compress(
                file_id=uploaded_file_id_2, # new version
                base_file_id=uploaded_file_id, # old version
                method="patch"
            )
            print(f"Diff Patch Result: {diff_patch_result}")

            # --- Restore from Diff Patch ---
            if "patch_filename" in diff_patch_result:
                patch_filename = diff_patch_result["patch_filename"]
                print(f"\n--- Restoring file from patch {patch_filename} using base {uploaded_file_id} ---")
                # For restore, file_id can be a new ID for the restored file, or just a placeholder
                restore_result = client.diff_compress(
                    file_id="restored_file_id", # A new ID for the restored file
                    base_file_id=uploaded_file_id, 
                    method="restore", 
                    patch_file_id=patch_filename # Use the actual filename of the patch
                )
                print(f"Restore Result: {restore_result}")
        except Exception as e:
            print(f"Diff/Patch example failed: {e}")

        # --- Get Compression Methods ---
        print(f"\n--- Getting Compression Methods ---")
        methods = client.get_compression_methods()
        print(f"Available Methods: {methods}")

    except HTTPException as e:
        print(f"API Error: {e.detail} (Status Code: {e.status_code})")
    except Exception as e:
        print(f"An unexpected error occurred during client operations: {e}")

    finally:
        # Clean up dummy files and downloaded files
        if os.path.exists(dummy_file_path): os.remove(dummy_file_path)
        if os.path.exists(dummy_file_path_2): os.remove(dummy_file_path_2)
        if os.path.exists(download_dir):
            import shutil
            shutil.rmtree(download_dir)
        print("\nCleanup complete.") 