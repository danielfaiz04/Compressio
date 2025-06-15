import os
from werkzeug.utils import secure_filename

def validate_file(file, allowed_extensions):
    """Validate if the file is allowed and has a valid extension."""
    if file.filename == '':
        return False, 'No file selected'
    
    filename = secure_filename(file.filename)
    if '.' not in filename:
        return False, 'No file extension'
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        return False, f'File type {ext} not allowed'
    
    return True, filename

def save_file(file, upload_folder):
    """Save the uploaded file to the specified folder."""
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return filepath

def get_file_size(filepath):
    """Get the size of a file in bytes."""
    return os.path.getsize(filepath)

def format_size(size_bytes):
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def ensure_directory(directory):
    """Ensure that a directory exists, create if it doesn't."""
    os.makedirs(directory, exist_ok=True) 