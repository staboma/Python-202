
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from library import Library
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Kütüphane API",
    description="Global AI Hub Python 202 Bootcamp Projesi için API",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001", "http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


lib = Library()

from typing import Optional

class BookModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


@app.get("/books")
def get_books():
    return {"books": [book.__dict__ for book in lib.books]}

@app.post("/books/{isbn}")
def add_book(isbn: str):
    if not lib.add_book_by_isbn(isbn):
        raise HTTPException(status_code=404, detail="Kitap eklenemedi.")
    return {"message": "Kitap eklendi"}

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    if not lib.find_book(isbn):
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    lib.remove_book(isbn)
    return {"message": "Kitap silindi"}

@app.put("/books/{isbn}")
def update_book(isbn: str, book_data: BookModel):
    if not lib.update_book(isbn, book_data.title, book_data.author, book_data.year):
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    return {"message": "Kitap güncellendi"}