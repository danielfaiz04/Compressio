import os
from sqlalchemy import create_engine
from .db_utils import Base, DATABASE_URL
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_db():
    """
    Initializes the database by creating all defined tables.
    """
    logging.info(f"Initializing database at {DATABASE_URL}...")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    logging.info("Database initialization complete.")

if __name__ == "__main__":
    init_db() 