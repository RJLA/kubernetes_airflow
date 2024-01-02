"""
This file contains the schemas for the Book model.
"""

from pydantic import BaseModel


class BookBase(BaseModel):
    """
    Book base schema representing the basic structure of a book.

    Attributes:
        title (str): The title of the book.
        author (str): The name of the book's author.
        publication_year (int): The year in which the book was published.
    """

    title: str
    author: str
    publication_year: int


class BookCreate(BookBase):
    """
    Book create schema extending the BookBase schema.

    This class is used for creating new book entries. It inherits all fields from BookBase.
    """
    pass


class Book(BookBase):
    """
    Book schema that extends the BookBase with additional attributes.

    Attributes:
        id (int): The unique identifier for the book.
        Config: A nested configuration class for Pydantic models.
    """
    id: int

    class Config:
        """
        Pydantic configuration class for the Book model.

        Attributes:
            orm_mode (bool): Enables ORM mode which allows the model to work with ORMs.
        """
        orm_mode = True


class UserBase(BaseModel):
    """
    User base schema representing the basic structure of a user.
    """
    email: str


class UserCreate(UserBase):
    """
    User create schema extending the UserBase schema.
    """
    password: str


class User(UserBase):
    """
    User schema that extends the UserBase with additional attributes.
    """
    id: int
    is_active: bool

    class Config:
        orm_mode = True
