from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    available_copies: int


class User(BaseModel):
    id: int
    name: str
    email: str


class BorrowRequest(BaseModel):
    user_id: int
    book_id: int


class ReturnRequest(BaseModel):
    user_id: int
    book_id: int


class BorrowRecord(BaseModel):
    record_id: int
    user_id: int
    book_id: int
    borrow_date: str
    due_date: str
    returned: bool
    fine: float


books_db: list[dict] = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin",
        "category": "Programming", "available_copies": 3},
    {"id": 2, "title": "Python Crash Course", "author": "Eric Matthes",
        "category": "Programming", "available_copies": 2},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald",
        "category": "Fiction", "available_copies": 5},
    {"id": 4, "title": "Atomic Habits", "author": "James Clear",
        "category": "Self-Help", "available_copies": 4},
    {"id": 5, "title": "Introduction to Algorithms", "author": "Thomas H. Cormen",
        "category": "Computer Science", "available_copies": 1},
]

users_db: list[dict] = [
    {"id": 1, "name": "Aminata Sesay", "email": "aminata@limkokwing.edu.sl"},
    {"id": 2, "name": "Mohamed Koroma", "email": "mohamed@limkokwing.edu.sl"},
    {"id": 3, "name": "Fatima Bangura", "email": "fatima@limkokwing.edu.sl"},
]

borrow_records_db: list[dict] = []
record_counter: int = 1


def find_book(book_id: int) -> Optional[dict]:
    for book in books_db:
        if book["id"] == book_id:
            return book
    return None


def find_user(user_id: int) -> Optional[dict]:

    for user in users_db:
        if user["id"] == user_id:
            return user
    return None


def calculate_fine(due_date_str: str) -> float:
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    today = datetime.today()
    if today > due_date:
        return round((today - due_date).days * 0.50, 2)
    return 0.0
