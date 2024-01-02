from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection information
USER = "root"
PW = "12345"
HOST = "localhost"
DBNAME = "booklibrary_db"

# Database URL
SQLALCHEMY_DATABASE_URL = f"mysql://{USER}:{PW}@{HOST}/{DBNAME}"

# Create the database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()
