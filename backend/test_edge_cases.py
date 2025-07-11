import requests
import os
import time
import logging
import io
from PIL import Image
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "http://localhost:8000"
API_KEY = "demo-key-123" # Use the default key for testing
HEADERS = {"X-API-Key": API_KEY}

UPLOAD_DIR = "./tmp/uploads_test"
DOWNLOAD_DIR = "./tmp/downloads_test"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def test_endpoint(endpoint: str, method: str, files=None, data=None, expected_status: int = 200, headers=HEADERS):
    url = f"{BASE_URL}{endpoint}"
    logging.info(f"Testing {method} {url} (expected: {expected_status})...")
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, files=files, data=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        logging.info(f"Response Status: {response.status_code}")
        logging.debug(f"Response Body: {response.text}")

        assert response.status_code == expected_status, \
            f"Expected status {expected_status} for {endpoint}, got {response.status_code}. Response: {response.text}"
        logging.info(f"Test passed for {endpoint}")
        return response.json() if response.content else {}
    except Exception as e:
        logging.error(f"Test failed for {endpoint}: {e}", exc_info=True)
        raise

def create_dummy_file(filename, size_mb=0.1, content_type="text/plain", is_corrupt=False):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if content_type.startswith("text/"):
        text_content = "a" * int(size_mb * 1024 * 1024 / len("a")) # Fill with 'a's
        if is_corrupt:
            text_content = text_content[:-10] + "corrupted"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text_content)
    elif content_type.startswith("image/"):
        img_size_pixels = int((size_mb * 1024 * 1024 / 3) ** 0.5) # Approx for RGB image
        img = Image.new('RGB', (img_size_pixels, img_size_pixels), color = 'red')
        if is_corrupt:
            # Simple corruption: write partial image data
            buffered = io.BytesIO()
            img.save(buffered, format='PNG')
            corrupt_data = buffered.getvalue()[:-100] # Cut off end
            with open(filepath, 'wb') as f:
                f.write(corrupt_data)
            logging.warning(f"Created a deliberately corrupted image file: {filepath}")
        else:
            img.save(filepath)
    elif content_type == "application/pdf":
        # Create a very simple PDF using pypdf
        from pypdf import PdfWriter
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        if is_corrupt:
            with open(filepath, "wb") as f: f.write(b"%PDF-1.4\n% This is a corrupted PDF\n")
            logging.warning(f"Created a deliberately corrupted PDF file: {filepath}")
        else:
            with open(filepath, "wb") as f: writer.write(f)
    else:
        # For other types, create a binary file
        with open(filepath, "wb") as f:
            f.write(os.urandom(int(size_mb * 1024 * 1024)))
            if is_corrupt:
                f.seek(0)
                f.write(b'\x00\x01\x02\x03') # Corrupt first few bytes
                logging.warning(f"Created a deliberately corrupted binary file: {filepath}")
    return filepath

def cleanup_test_dirs():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def run_edge_case_tests():
    logging.info("\n--- Running Edge Case Tests ---")
    cleanup_test_dirs()

    # Test 1: Upload a large file (exceeding MAX_UPLOAD_SIZE_MB)
    logging.info("\n--- Test: Upload too large file (expected 400) ---")
    large_filename = "large_file.txt"
    large_filepath = create_dummy_file(large_filename, size_mb=6) # Default MAX_UPLOAD_SIZE_MB is 5
    try:
        with open(large_filepath, 'rb') as f:
            test_endpoint("/upload", "POST", files={'file': (large_filename, f, 'text/plain')}, expected_status=400)
    finally:
        os.remove(large_filepath)

    # Test 2: Upload a zero-byte file
    logging.info("\n--- Test: Upload zero-byte file ---")
    zero_byte_filename = "zero_byte.txt"
    zero_byte_filepath = create_dummy_file(zero_byte_filename, size_mb=0)
    uploaded_zero_id = None
    try:
        with open(zero_byte_filepath, 'rb') as f:
            response = test_endpoint("/upload", "POST", files={'file': (zero_byte_filename, f, 'text/plain')}, expected_status=202)
        uploaded_zero_id = response['id']
        # Compression of zero-byte file might not change size, or could error depending on method
        test_endpoint("/compress", "POST", data={'file_id': uploaded_zero_id, 'method': 'gzip'}, expected_status=200)
        result = test_endpoint(f"/result/{uploaded_zero_id}", "GET")
        assert result['size_before'] == 0
        # assert result['size_after'] == 0 # Depending on gzip overhead, it might be small non-zero
        logging.info("Zero-byte file upload and compression handled.")
    finally:
        if uploaded_zero_id: # Clean up associated files if upload succeeded
            cleanup_old_files_manual(uploaded_zero_id)
        os.remove(zero_byte_filepath)

    # Test 3: Upload a corrupted image file and attempt compression
    logging.info("\n--- Test: Upload corrupted image (expected 500 on compress) ---")
    corrupt_img_filename = "corrupt_image.png"
    corrupt_img_filepath = create_dummy_file(corrupt_img_filename, content_type="image/png", is_corrupt=True)
    uploaded_corrupt_img_id = None
    try:
        with open(corrupt_img_filepath, 'rb') as f:
            response = test_endpoint("/upload", "POST", files={'file': (corrupt_img_filename, f, 'image/png')}, expected_status=202)
        uploaded_corrupt_img_id = response['id']
        # Expecting 500 as Pillow or optimization library will fail on corrupt image
        test_endpoint("/compress", "POST", data={'file_id': uploaded_corrupt_img_id, 'method': 'webp'}, expected_status=500)
        logging.info("Corrupted image file correctly caused compression failure.")
    finally:
        if uploaded_corrupt_img_id:
            cleanup_old_files_manual(uploaded_corrupt_img_id)
        os.remove(corrupt_img_filepath)

    # Test 4: Upload a corrupted PDF file and attempt compression
    logging.info("\n--- Test: Upload corrupted PDF (expected 500 on compress) ---")
    corrupt_pdf_filename = "corrupt_doc.pdf"
    corrupt_pdf_filepath = create_dummy_file(corrupt_pdf_filename, content_type="application/pdf", is_corrupt=True)
    uploaded_corrupt_pdf_id = None
    try:
        with open(corrupt_pdf_filepath, 'rb') as f:
            response = test_endpoint("/upload", "POST", files={'file': (corrupt_pdf_filename, f, 'application/pdf')}, expected_status=202)
        uploaded_corrupt_pdf_id = response['id']
        # Expecting 500 as pypdf or optimization will fail
        test_endpoint("/compress", "POST", data={'file_id': uploaded_corrupt_pdf_id, 'method': 'pdf_optimize'}, expected_status=500)
        logging.info("Corrupted PDF file correctly caused compression failure.")
    finally:
        if uploaded_corrupt_pdf_id:
            cleanup_old_files_manual(uploaded_corrupt_pdf_id)
        os.remove(corrupt_pdf_filepath)

    # Test 5: Request non-existent file ID for result/download/compare
    logging.info("\n--- Test: Non-existent file ID (expected 404) ---")
    non_existent_id = "non_existent_12345"
    test_endpoint(f"/result/{non_existent_id}", "GET", expected_status=404)
    test_endpoint(f"/download/{non_existent_id}", "GET", expected_status=404)
    test_endpoint(f"/compare/{non_existent_id}", "GET", expected_status=404)

    # Test 6: Duplicate file uploads (should be treated as new distinct files)
    logging.info("\n--- Test: Duplicate file upload ---")
    dup_filename = "duplicate.txt"
    dup_filepath = create_dummy_file(dup_filename, content="This is a duplicate file.")
    uploaded_dup_id1 = None
    uploaded_dup_id2 = None
    try:
        with open(dup_filepath, 'rb') as f:
            response1 = test_endpoint("/upload", "POST", files={'file': (dup_filename, f, 'text/plain')}, expected_status=202)
        uploaded_dup_id1 = response1['id']
        
        with open(dup_filepath, 'rb') as f:
            response2 = test_endpoint("/upload", "POST", files={'file': (dup_filename, f, 'text/plain')}, expected_status=202)
        uploaded_dup_id2 = response2['id']
        
        assert uploaded_dup_id1 != uploaded_dup_id2, "Duplicate upload should result in different IDs."
        logging.info(f"Duplicate uploads got distinct IDs: {uploaded_dup_id1} and {uploaded_dup_id2}")
    finally:
        if uploaded_dup_id1: cleanup_old_files_manual(uploaded_dup_id1)
        if uploaded_dup_id2: cleanup_old_files_manual(uploaded_dup_id2)
        os.remove(dup_filepath)

    # Test 7: Sensitive mode for non-text file (should not detect, but not fail)
    logging.info("\n--- Test: Sensitive mode on non-text file ---")
    img_filename_sensitive = "image_for_sensitive_test.png"
    img_filepath_sensitive = create_dummy_file(img_filename_sensitive, content_type="image/png")
    uploaded_img_sensitive_id = None
    try:
        with open(img_filepath_sensitive, 'rb') as f:
            response = test_endpoint("/upload", "POST", files={'file': (img_filename_sensitive, f, 'image/png')}, expected_status=202)
        uploaded_img_sensitive_id = response['id']
        
        compress_response = test_endpoint("/compress", "POST", 
                                          data={'file_id': uploaded_img_sensitive_id, 'method': 'webp', 'sensitive_mode': True},
                                          expected_status=200)
        assert not compress_response['sensitive_entities_detected'], "Sensitive detection should not trigger for image."
        logging.info("Sensitive mode on image correctly resulted in no detection.")
    finally:
        if uploaded_img_sensitive_id: cleanup_old_files_manual(uploaded_img_sensitive_id)
        os.remove(img_filepath_sensitive)

    logging.info("\nAll Edge Case tests finished successfully!")
    cleanup_test_dirs()

# Helper for manual cleanup for tests (since cleanup_old_files needs SessionLocal)
def cleanup_old_files_manual(file_id: str):
    # This is a simplified manual cleanup for test files. 
    # In a real scenario, the main cleanup job would handle this.
    for d in [UPLOAD_DIR, DOWNLOAD_DIR]:
        for f_name in os.listdir(d):
            if file_id in f_name:
                os.remove(os.path.join(d, f_name))
                logging.info(f"Manually cleaned up: {os.path.join(d, f_name)}")

if __name__ == "__main__":
    run_edge_case_tests() 