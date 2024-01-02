# test_main.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_book():
    response = client.post("/books/", json={"title": "New Book", "author": "Author", "publication_year": 2021})
    assert response.status_code == 200
    assert response.json()["title"] == "New Book"


def test_read_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_delete_book():
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Book deleted"}
