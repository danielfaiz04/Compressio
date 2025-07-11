import os
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ai_select_compression_method(file_path: str, mime_type: str, user_profile: Optional[str] = None) -> Tuple[str, str]:
    """
    AI-driven function to select the best compression method and profile.
    This is a simplified rule-based AI selector. In a real-world scenario,
    this would involve ML models trained on various file types and compression results.

    Args:
        file_path (str): The path to the file to be compressed.
        mime_type (str): The MIME type of the file.
        user_profile (Optional[str]): User preference for compression profile 
                                      ('web', 'archive', 'network', 'default').

    Returns:
        Tuple[str, str]: A tuple containing the selected compression method and the chosen profile.
    """
    file_size = os.path.getsize(file_path) # in bytes
    
    # Determine file category
    if mime_type.startswith('image/'):
        file_category = "image"
    elif mime_type == 'application/pdf':
        file_category = "pdf"
    elif mime_type.startswith('video/'):
        file_category = "video"
    elif mime_type.startswith('audio/'):
        file_category = "audio"
    elif mime_type.startswith('text/') or mime_type == 'application/json':
        file_category = "text"
    elif mime_type in [
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    ]:
        file_category = "document"
    elif mime_type in ['application/zip', 'application/x-tar', 'application/x-rar-compressed']:
        file_category = "archive"
    else:
        file_category = "other"

    selected_method = "gzip" # Default fallback
    selected_profile = user_profile if user_profile else "default"

    logging.info(f"AI Selection: Analyzing file (size: {file_size} bytes, type: {mime_type}, category: {file_category}, user_profile: {user_profile})")

    if file_category == "image":
        if selected_profile == "web" or file_size > 500 * 1024: # > 500KB
            selected_method = "webp" # Best for web images
            selected_profile = "web"
        else:
            selected_method = "gzip" # General compression for smaller images or non-web use
            selected_profile = "default"
    elif file_category == "pdf":
        selected_method = "pdf_optimize"
        selected_profile = "archive" # PDF optimization aims for maximum reduction
    elif file_category == "video":
        selected_method = "video_optimize"
        selected_profile = "network" # Video optimization often for streaming/network
    elif file_category == "document":
        selected_method = "office_optimize"
        selected_profile = "archive"
    elif file_category == "text":
        if selected_profile == "network": # For fast transfer over network
            selected_method = "brotli"
        elif selected_profile == "archive": # For maximum compression
            selected_method = "gzip" # Or lzma if added
        else:
            selected_method = "brotli" # Brotli is generally good for text
            selected_profile = "default"
    elif file_category == "archive":
        selected_method = "gzip" # Archives are often already compressed, gzip can add a layer if needed
        selected_profile = "archive"
    else: # Fallback for 'other' types
        selected_method = "gzip"
        selected_profile = "default"

    logging.info(f"AI Selected Method: {selected_method}, Profile: {selected_profile}")
    return selected_method, selected_profile

if __name__ == "__main__":
    # This is a placeholder for testing the AI selector logic directly.
    # In a real application, you would pass actual file paths and MIME types.
    print("Running AI selection examples:")

    # Create dummy files for testing purposes
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    with open("tmp/test_image.jpg", "wb") as f: f.write(os.urandom(1024 * 600)) # 600KB
    with open("tmp/test_pdf.pdf", "wb") as f: f.write(os.urandom(1024 * 100)) # 100KB
    with open("tmp/test_text.txt", "w") as f: f.write("Hello world!" * 1000)

    print("\nImage file (600KB), default profile:")
    method, profile = ai_select_compression_method("tmp/test_image.jpg", "image/jpeg")
    print(f"  Method: {method}, Profile: {profile}") # Expected: webp, web

    print("\nImage file (600KB), archive profile:")
    method, profile = ai_select_compression_method("tmp/test_image.jpg", "image/jpeg", user_profile="archive")
    print(f"  Method: {method}, Profile: {profile}") # Expected: webp, web (overrides user profile if AI deems better)

    print("\nPDF file, default profile:")
    method, profile = ai_select_compression_method("tmp/test_pdf.pdf", "application/pdf")
    print(f"  Method: {method}, Profile: {profile}") # Expected: pdf_optimize, archive

    print("\nText file, network profile:")
    method, profile = ai_select_compression_method("tmp/test_text.txt", "text/plain", user_profile="network")
    print(f"  Method: {method}, Profile: {profile}") # Expected: brotli, network

    print("\nUnknown file type, default profile:")
    method, profile = ai_select_compression_method("tmp/unknown.bin", "application/octet-stream")
    print(f"  Method: {method}, Profile: {profile}") # Expected: gzip, default

    # Clean up dummy files
    os.remove("tmp/test_image.jpg")
    os.remove("tmp/test_pdf.pdf")
    os.remove("tmp/test_text.txt")
    os.rmdir("tmp") 