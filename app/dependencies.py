"""
This file contains the functions that will be used to interact with the database.
"""
from sqlalchemy.orm import Session
from app.models import Book
from app.models import User
from app.schemas import BookCreate
from app.schemas import UserCreate
from app.auth import get_password_hash


class BookManager:
    """
    BookManager class containing functions to interact with the database.
    """

    def get_books(self, db: Session):
        """
        Retrieves all books from the database.
        The query translates to the following SQL statement:
        SELECT * FROM books;

        Args:
            db (Session): A SQLAlchemy database session.
        """
        return db.query(Book).all()

    def get_book(self, db: Session, book_id: int):
        """
        Retrieves a book from the database based on its ID.
        The query translates to the following SQL statement:
        SELECT * FROM books WHERE id = book_id;

        Args:
            db (Session): A SQLAlchemy database session.
            book_id (int): The ID of the book to retrieve.
        """
        return db.query(Book).filter(Book.id == book_id).first()

    def add_book(self, db: Session, book_data: BookCreate):
        """
        Adds a new book to the database.
        The query translates to the following SQL statement:
        INSERT INTO books (title, author, publication_year)
        VALUES (book_data.title, book_data.author, book_data.publication_year);

        Args:
            db (Session): A SQLAlchemy database session.
            book_data (BookCreate): A Pydantic model representing the book to be added.
        """
        book = Book(**book_data.model_dump())
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    def delete_book(self, db: Session, book_id: int):
        """
        Deletes a book from the database based on its ID.
        The query translates to the following SQL statement:
        DELETE FROM books WHERE id = book_id;

        Args:
            db (Session): A SQLAlchemy database session.
            book_id (int): The ID of the book to delete.
        """
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            db.delete(book)
            db.commit()
            return True
        return False

    def update_book(self, db: Session, book_id: int, book_data: BookCreate):
        """
        Updates a book in the database based on its ID.
        The query translates to the following SQL statement:
        UPDATE books
        SET title = book_data.title, author = book_data.author, publication_year = book_data.publication_year
        WHERE id = book_id;

        Args:
            db (Session): A SQLAlchemy database session.
            book_id (int): The ID of the book to update.
            book_data (BookCreate): A Pydantic model representing the book to be updated.
        """
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            book.title = book_data.title
            book.author = book_data.author
            book.publication_year = book_data.publication_year
            db.commit()
            return True
        return False


class UserManager:
    """
    UserManager class containing functions to interact with the database.
    """

    def create_user(self, db: Session, user: UserCreate):
        """
        Creates a new user in the database.

        Args:
            db (Session): A SQLAlchemy database session.
            user (UserCreate): A Pydantic model representing the user to be created.
        """
        db_user = User(email=user.email, hashed_password=get_password_hash(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
