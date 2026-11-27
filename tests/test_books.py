import os
import tempfile
TEST_DB_FILE = os.path.join(
    tempfile.gettempdir(),
    "betzytech_test.db"
)

os.environ["DATABASE_PATH"] = TEST_DB_FILE

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import Base, get_db
from backend.main import app
from fastapi.testclient import TestClient


# Create an isolated in-memory test database
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# Create test tables
Base.metadata.create_all(bind=test_engine)


# Override the application's database dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def seed_test_book():
    from backend.models import BookDB

    db = TestingSessionLocal()
    try:
        book = BookDB(
            title="Test Book",
            author="Test Author",
            category="Testing",
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book.id
    finally:
        db.close()
        
def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to BetzyTech Library API"
    }

def test_get_all_books():
    response = client.get("/api/books")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_book():
    book_id = seed_test_book()

    response = client.get(f"/api/books/{book_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"
    assert response.json()["author"] == "Test Author"

def test_get_missing_book():
    response = client.get("/api/books/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_create_book():
    new_book = {
        "title": "Learning DevOps",
        "author": "Test Author",
        "category": "Technology"
    }

    response = client.post("/api/books", json=new_book)

    assert response.status_code == 201
    assert response.json()["title"] == "Learning DevOps"
    assert response.json()["author"] == "Test Author"

def test_update_book():
    book_id = seed_test_book()

    updated_book = {
        "title": "Updated DevOps Book",
        "author": "Updated Author",
        "category": "Cloud Computing"
    }

    response = client.put(
        f"/api/books/{book_id}",
        json=updated_book
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated DevOps Book"
    assert response.json()["author"] == "Updated Author"
    assert response.json()["category"] == "Cloud Computing"

def test_delete_book():
    book_id = seed_test_book()

    response = client.delete(f"/api/books/{book_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"

    # Confirm the book no longer exists
    check_response = client.get(f"/api/books/{book_id}")
    assert check_response.status_code == 404

def test_search_books():
    seed_test_book()

    response = client.get("/api/books/search?keyword=Test")

    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["title"] == "Test Book"

def test_create_book_with_missing_title():
    invalid_book = {
        "title": "",
        "author": "Test Author",
        "category": "Technology"
    }

    response = client.post("/api/books", json=invalid_book)

    assert response.status_code == 422







