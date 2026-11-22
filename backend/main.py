from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import get_db, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from backend import models
from backend.database import engine, Base

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator

class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    category: str = Field(min_length=1)
    
    @field_validator("title", "author", "category")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty or contain only spaces")

        return value

app = FastAPI(title="BetzyTech Library API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8083",
        "http://127.0.0.1:8083",
        "http://localhost:8084",
        "http://127.0.0.1:8084",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
def seed_books():
    db = SessionLocal()

    try:
        if db.query(models.BookDB).count() == 0:
            sample_books = [
                models.BookDB(
                    title="Clean Code",
                    author="Robert C. Martin",
                    category="Software Development"
                ),
                models.BookDB(
                    title="The Phoenix Project",
                    author="Gene Kim",
                    category="DevOps"
                ),
                models.BookDB(
                    title="Learning Python",
                    author="Mark Lutz",
                    category="Programming"
                )
            ]

            db.add_all(sample_books)
            db.commit()

    finally:
        db.close()


seed_books()

books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Software Development"
    },
    {
        "id": 2,
        "title": "The Phoenix Project",
        "author": "Gene Kim",
        "category": "DevOps"
    },
    {
        "id": 3,
        "title": "Learning Python",
        "author": "Mark Lutz",
        "category": "Programming"
    }
]

@app.get("/")
def home():
    return {"message": "Welcome to BetzyTech Library API"}

@app.get("/api/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(models.BookDB).all()

@app.get("/api/books/search")
def search_books(keyword: str, db: Session = Depends(get_db)):
    results = db.query(models.BookDB).filter(
        models.BookDB.title.ilike(f"%{keyword}%") |
        models.BookDB.author.ilike(f"%{keyword}%") |
        models.BookDB.category.ilike(f"%{keyword}%")
    ).all()

    return results

@app.get("/api/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.BookDB).filter(
        models.BookDB.id == book_id
    ).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@app.post("/api/books")
def add_book(book: Book, db: Session = Depends(get_db)):
    new_book = models.BookDB(
        title=book.title,
        author=book.author,
        category=book.category
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@app.put("/api/books/{book_id}")
def update_book(
    book_id: int,
    updated_book: Book,
    db: Session = Depends(get_db)
):
    book = db.query(models.BookDB).filter(
        models.BookDB.id == book_id
    ).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = updated_book.title
    book.author = updated_book.author
    book.category = updated_book.category

    db.commit()
    db.refresh(book)

    return book

@app.delete("/api/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.BookDB).filter(
        models.BookDB.id == book_id
    ).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}
