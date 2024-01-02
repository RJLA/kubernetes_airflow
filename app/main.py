from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth import verify_password, create_access_token
from app.dependencies import UserManager
from app import schemas, dependencies
from app.database import SessionLocal

app = FastAPI()


# Function to get a database session
def get_db():
    """
    Creates a new database session for each request.

    Returns:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()  # Create a new local session
    try:  # Yield the session to the request
        yield db  # Yield is a keyword that is used like return, except the function will return a generator.
    finally:  # Close the session after the request is complete
        db.close()  # Close the session


# Instantiate the BookManager
book_manager = dependencies.BookManager()


@app.get("/books/", response_model=list[schemas.Book])
def list_books(db: Session = Depends(get_db)):
    """
    Retrieves a list of all books in the database.

    Args:
        db (Session): A SQLAlchemy database session.
    """
    return book_manager.get_books(db)


@app.post("/books/", response_model=schemas.Book)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Adds a new book to the database.

    Args:
        book (BookCreate): A Pydantic model representing the book to be added.
        db (Session): A SQLAlchemy database session.
    """
    return book_manager.add_book(db, book)


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a book from the database based on its ID.

    Args:
        book_id (int): The ID of the book to retrieve.
        db (Session): A SQLAlchemy database session.
    """
    book = book_manager.get_book(db, book_id)  # Get the book from the database
    if book is None:  # If the book is not found, raise an HTTPException
        raise HTTPException(status_code=404, detail="Book not found")
    return book  # Return the book


@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Deletes a book from the database based on its ID.

    Args:
        book_id (int): The ID of the book to delete.
        db (Session): A SQLAlchemy database session.
    """
    result = book_manager.delete_book(db, book_id)  # Delete the book from the database
    if not result:  # If the book is not found, raise an HTTPException
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}  # Return a success message


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Updates a book in the database based on its ID.

    Args:
        book_id (int): The ID of the book to update.
        book (BookCreate): A Pydantic model representing the book to be updated.
        db (Session): A SQLAlchemy database session.
    """
    result = book_manager.update_book(db, book_id, book)  # Update the book in the database
    if not result:  # If the book is not found, raise an HTTPException
        raise HTTPException(status_code=404, detail="Book not found")
    return book_manager.get_book(db, book_id)  # Return the updated book


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_manager = UserManager()
    return user_manager.create_user(db, user)


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_manager = UserManager()
    user = user_manager.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
