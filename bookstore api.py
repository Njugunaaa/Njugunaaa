from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str = None

books = []

@app.get("/")
def root():
    return {"message": "Welcome to the Bookstore API!"}

@app.get("/books/")
def get_books():
    return {"books": books}

@app.post("/books/")
def add_book(book: Book):

    for b in books:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists.")
    books.append(book)
    return {"message": "Book added successfully", "book": book}

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found.")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found.")
