import os
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cleanup_old_files(upload_dir: str, download_dir: str, lifespan_hours: int, SessionLocal):
    """
    Cleans up old files in upload and download directories and corresponding database metadata.
    """
    logging.info(f"Starting cleanup process for files older than {lifespan_hours} hours...")
    
    cutoff_time = datetime.utcnow() - timedelta(hours=lifespan_hours)

    db = SessionLocal()
    try:
        from .main import FileMetadata # Import dynamically to avoid circular dependency

        # Query for files older than cutoff_time
        old_files_metadata = db.query(FileMetadata).filter(FileMetadata.last_accessed < cutoff_time).all()

        for meta in old_files_metadata:
            original_file_path = os.path.join(upload_dir, f"{meta.id}_{meta.original_filename}")
            compressed_file_path = os.path.join(download_dir, meta.compressed_filename) if meta.compressed_filename else None

            if os.path.exists(original_file_path):
                os.remove(original_file_path)
                logging.info(f"Deleted old original file: {original_file_path}")
            
            if compressed_file_path and os.path.exists(compressed_file_path):
                os.remove(compressed_file_path)
                logging.info(f"Deleted old compressed file: {compressed_file_path}")
            
            db.delete(meta)
            logging.info(f"Deleted metadata for file ID: {meta.id}")
        
        db.commit()
        logging.info(f"Cleanup complete. {len(old_files_metadata)} files and their metadata purged.")

    except Exception as e:
        db.rollback()
        logging.error(f"Error during cleanup process: {e}", exc_info=True)
    finally:
        db.close()

if __name__ == "__main__":
    # This part is for standalone testing or manual execution
    # In a real FastAPI app, this function would be called by a scheduler
    print("This script is intended to be run as part of the FastAPI application's background tasks.")
    print("To test, you would typically import and call cleanup_old_files with appropriate parameters.")
    # Example usage (requires a configured database and temp directories)
    # from main import SessionLocal, UPLOAD_DIR, DOWNLOAD_DIR, FILE_LIFESPAN_HOURS
    # cleanup_old_files(UPLOAD_DIR, DOWNLOAD_DIR, FILE_LIFESPAN_HOURS, SessionLocal) 