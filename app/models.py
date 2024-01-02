"""
Book model for the application
"""

from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Book(Base):
    """
    Book model
    Contains the following fields:
    - id: int
    - title: str
    - author: str
    - publication_year: int
    """
    __tablename__ = "books"  # Table name

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer)


class User(Base):
    """
    User model
    Contains the following fields:
    - id: int
    - username: str
    - email: str
    - hashed_password: str
    - is_active: bool
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
