from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

app = FastAPI(title="City Public Library API")

class MemberType(str, Enum):
    REGULAR = "regular"
    PREMIUM = "premium"

class NewBook(BaseModel):
    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    is_available: bool = True

class BorrowRequest(BaseModel):
    member_name: str = Field(..., min_length=2)
    book_id: int = Field(..., gt=0)
    borrow_days: int = Field(..., gt=0, le=30)
    member_id: str = Field(..., min_length=4)
    member_type: MemberType = MemberType.REGULAR

books: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "title": "Python Basics", "author": "John", "genre": "Tech", "is_available": True},
    2: {"id": 2, "title": "History of India", "author": "Ram", "genre": "History", "is_available": True},
    3: {"id": 3, "title": "AI Future", "author": "Elon", "genre": "Tech", "is_available": False},
}
borrow_records: List[Dict[str, Any]] = []
queue: List[Dict[str, Any]] = []

book_id_counter = 4
record_counter = 1

def get_book_or_404(book_id: int):
    book = books.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

def calculate_due_date(days: int, member_type: MemberType):
    max_days = 60 if member_type == MemberType.PREMIUM else 30
    return f"Return by Day {15 + min(days, max_days)}"

@app.get("/")
def home():
    return {"message": "Welcome to Library API"}

@app.get("/books")
def get_books():
    return {
        "total": len(books),
        "books": list(books.values())
    }

@app.get("/books/summary")
def summary():
    return {
        "total": len(books),
        "available": sum(1 for b in books.values() if b["is_available"])
    }

@app.get("/books/{book_id}")
def get_book(book_id: int):
    return get_book_or_404(book_id)

@app.get("/borrow-records")
def get_records():
    return borrow_records

@app.post("/books", status_code=201)
def add_book(book: NewBook):
    global book_id_counter

    new_book = {"id": book_id_counter, **book.model_dump()}
    books[book_id_counter] = new_book
    book_id_counter += 1

    return new_book

@app.post("/borrow", status_code=201)
def borrow_book(req: BorrowRequest):
    global record_counter

    book = get_book_or_404(req.book_id)

    if not book["is_available"]:
        raise HTTPException(400, "Book not available")

    book["is_available"] = False

    record = {
        "record_id": record_counter,
        "member_name": req.member_name,
        "book_id": req.book_id,
        "due_date": calculate_due_date(req.borrow_days, req.member_type)
    }

    borrow_records.append(record)
    record_counter += 1

    return record

@app.put("/books/{book_id}")
def update_book(book_id: int, genre: Optional[str] = None):
    book = get_book_or_404(book_id)

    if genre:
        book["genre"] = genre

    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    get_book_or_404(book_id)
    del books[book_id]
    return {"message": "Deleted"}
@app.post("/queue/add")
def add_queue(member_name: str, book_id: int):
    book = get_book_or_404(book_id)

    if book["is_available"]:
        return {"message": "Book available"}

    queue.append({"member_name": member_name, "book_id": book_id})
    return {"message": "Added to queue"}

@app.get("/queue")
def get_queue():
    return queue

@app.post("/return/{book_id}")
def return_book(book_id: int):
    global record_counter

    book = get_book_or_404(book_id)

    waiting = next((p for p in queue if p["book_id"] == book_id), None)

    if waiting:
        queue.remove(waiting)

        record = {
            "record_id": record_counter,
            "member_name": waiting["member_name"],
            "book_id": book_id,
            "due_date": "Auto-assigned"
        }

        borrow_records.append(record)
        record_counter += 1

        return {"message": "Reassigned"}

    book["is_available"] = True
    return {"message": "Returned"}

@app.get("/books/search")
def search_books(keyword: str):
    return [b for b in books.values() if keyword.lower() in b["title"].lower()]

@app.get("/books/sort")
def sort_books(sort_by: str = "title"):
    return sorted(books.values(), key=lambda x: x[sort_by])

@app.get("/books/page")
def paginate(page: int = 1, limit: int = 2):
    data = list(books.values())
    start = (page - 1) * limit
    return data[start:start + limit]

@app.get("/books/filter")
def filter_books(genre: Optional[str] = None):
    result = list(books.values())
    if genre:
        result = [b for b in result if b["genre"].lower() == genre.lower()]
    return result

@app.get("/books/browse")
def browse(page: int = 1, limit: int = 2):
    data = list(books.values())
    start = (page - 1) * limit
    return data[start:start + limit]

@app.get("/books/available")
def available_books():
    return [b for b in books.values() if b["is_available"]]

@app.get("/borrow-records/search")
def search_records(member_name: str):
    return [r for r in borrow_records if member_name.lower() in r["member_name"].lower()]

@app.get("/borrow-records/page")
def paginate_records(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return borrow_records[start:start + limit]