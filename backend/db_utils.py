import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the database URL from environment variable or default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tmp/results_db.sqlite3")

# Ensure the directory for the database exists
os.makedirs(os.path.dirname(DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

Base = declarative_base()

class FileMetadata(Base):
    __tablename__ = "file_metadata"
    id = Column(String, primary_key=True, index=True)
    original_filename = Column(String)
    compressed_filename = Column(String, nullable=True)
    mime_type = Column(String)
    size_before = Column(Integer)
    size_after = Column(Integer, nullable=True)
    compression_method = Column(String, nullable=True)
    ratio = Column(Float, nullable=True)
    elapsed_time = Column(Float, nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    sensitive_entities_detected = Column(Boolean, default=False)
    sensitive_entities_summary = Column(Text, nullable=True)
    decompression_time_ms = Column(Float, nullable=True)
    diff_summary = Column(Text, nullable=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initializes the database by creating all defined tables.
    """
    logging.info(f"Initializing database at {DATABASE_URL}...")
    Base.metadata.create_all(engine)
    logging.info("Database initialization complete.")

def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    # Example usage for direct database initialization
    init_db()
    logging.info("Database initialized via direct script execution.")

    # Example of adding a record
    # db = SessionLocal()
    # try:
    #     new_entry = FileMetadata(
    #         id="test_id_123",
    #         original_filename="test_file.txt",
    #         mime_type="text/plain",
    #         size_before=1000,
    #         upload_time=datetime.utcnow()
    #     )
    #     db.add(new_entry)
    #     db.commit()
    #     db.refresh(new_entry)
    #     print(f"Added new entry: {new_entry.id}")
    # finally:
    #     db.close() 