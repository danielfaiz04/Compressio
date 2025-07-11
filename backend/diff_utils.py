import os
from diff_match_patch import diff_match_patch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_diff_patch(file1_path: str, file2_path: str) -> bytes:
    """
    Creates a binary diff patch between two files.
    Reads files as binary and generates a diff.
    """
    dmp = diff_match_patch()
    
    try:
        with open(file1_path, 'rb') as f1:
            text1 = f1.read()
        with open(file2_path, 'rb') as f2:
            text2 = f2.read()
    except FileNotFoundError:
        logging.error("One or both input files for diff not found.")
        raise FileNotFoundError("One or both input files for diff not found.")
    except Exception as e:
        logging.error(f"Error reading files for diff: {e}")
        raise

    # Convert bytes to string for diff_match_patch (it operates on Unicode strings)
    # This might be an issue for truly binary files. A robust solution might involve
    # base64 encoding or a library that handles binary diff directly.
    # For now, we assume text-like binary or handle encoding errors.
    try:
        str1 = text1.decode('utf-8', errors='ignore')
        str2 = text2.decode('utf-8', errors='ignore')
    except UnicodeDecodeError:
        logging.warning("Could not decode files as UTF-8 for diff. Proceeding with ignored errors.")
        str1 = text1.decode('latin-1', errors='ignore') # Fallback to a single-byte encoding
        str2 = text2.decode('latin-1', errors='ignore')

    # Generate diffs
    diffs = dmp.diff_main(str1, str2)
    dmp.diff_cleanupSemantic(diffs)
    
    # Create patch
    patches = dmp.patch_make(diffs)
    patch_text = dmp.patch_toText(patches)
    
    return patch_text.encode('utf-8') # Encode patch back to bytes

def apply_diff_patch(base_file_path: str, patch_file_path: str, output_file_path: str):
    """
    Applies a binary diff patch to a base file to reconstruct the target file.
    """
    dmp = diff_match_patch()

    try:
        with open(base_file_path, 'rb') as f_base:
            base_text = f_base.read()
        with open(patch_file_path, 'rb') as f_patch:
            patch_text = f_patch.read().decode('utf-8')
    except FileNotFoundError:
        logging.error("Base file or patch file not found for applying diff.")
        raise FileNotFoundError("Base file or patch file not found for applying diff.")
    except Exception as e:
        logging.error(f"Error reading files for applying diff: {e}")
        raise
    
    try:
        base_str = base_text.decode('utf-8', errors='ignore')
    except UnicodeDecodeError:
        base_str = base_text.decode('latin-1', errors='ignore')

    patches = dmp.patch_fromText(patch_text)
    new_text, results = dmp.patch_apply(patches, base_str)
    
    if all(results):
        try:
            with open(output_file_path, 'wb') as f_out:
                f_out.write(new_text.encode('utf-8'))
            logging.info(f"Successfully applied patch to {base_file_path} and saved to {output_file_path}")
        except Exception as e:
            logging.error(f"Error writing output file after patch application: {e}")
            raise
    else:
        logging.error(f"Failed to apply patch fully. Results: {results}")
        raise Exception("Failed to apply patch fully.")

if __name__ == "__main__":
    # Example Usage (for testing locally)
    # Create dummy files
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    
    file1_content = b"This is the original file.\nIt has some content.\nLine 3.\n"
    file2_content = b"This is the updated file.\nIt has some modified content.\nLine 3.\nNew line 4."

    with open("tmp/file1.txt", 'wb') as f: f.write(file1_content)
    with open("tmp/file2.txt", 'wb') as f: f.write(file2_content)

    print("Creating diff patch...")
    patch_data = create_diff_patch("tmp/file1.txt", "tmp/file2.txt")
    with open("tmp/patch.bin", 'wb') as f: f.write(patch_data)
    print(f"Patch created and saved to tmp/patch.bin (size: {len(patch_data)} bytes)")

    print("Applying diff patch...")
    apply_diff_patch("tmp/file1.txt", "tmp/patch.bin", "tmp/restored_file.txt")

    with open("tmp/restored_file.txt", 'rb') as f: restored_content = f.read()
    print(f"Restored file content: {restored_content}")

    if restored_content == file2_content:
        print("Diff and patch successful!")
    else:
        print("Diff and patch failed.")

    # Clean up dummy files
    os.remove("tmp/file1.txt")
    os.remove("tmp/file2.txt")
    os.remove("tmp/patch.bin")
    os.remove("tmp/restored_file.txt")
    os.rmdir("tmp") 