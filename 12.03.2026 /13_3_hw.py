from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

books = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "description": "Fantasy novel"},
    {"id": 2, "title": "1984", "author": "George Orwell", "year": 1949, "description": "Dystopian novel"},
    {"id": 3, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008, "description": "Software dev practices"},
]

next_id = 4

class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    description: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None

def find_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return None

@app.get("/books")
def get_all_books():
    return {"books": books}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return book


@app.post("/books", status_code=201)
def create_book(data: BookCreate):
    global next_id
    new_book = {
        "id": next_id,
        "title": data.title,
        "author": data.author,
        "year": data.year,
        "description": data.description,
    }
    books.append(new_book)
    next_id += 1
    return {"message": "Book created successfully", "book": new_book}


@app.put("/books/{book_id}")
def replace_book(book_id: int, data: BookCreate):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    book["title"] = data.title
    book["author"] = data.author
    book["year"] = data.year
    book["description"] = data.description
    return {"message": "Book replaced successfully", "book": book}


@app.patch("/books/{book_id}")
def update_book(book_id: int, data: BookUpdate):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    update_data = data.model_dump(exclude_unset=True)
    book.update(update_data)
    return {"message": "Book updated successfully", "book": book}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    books.remove(book)
    return {"message": "Book deleted successfully", "book": book}
