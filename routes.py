from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from typing import Optional
import asyncio

from models import (
    User, BorrowRequest, ReturnRequest,
    books_db, users_db, borrow_records_db,
    find_book, find_user, calculate_fine
)
import models

router = APIRouter()


@router.get("/books", tags=["Books"])
async def get_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    category: Optional[str] = None
):
    results = books_db.copy()
    if title:
        results = [b for b in results if title.lower() in b["title"].lower()]
    if author:
        results = [b for b in results if author.lower() in b["author"].lower()]
    if category:
        results = [b for b in results if category.lower()
                   in b["category"].lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No books found.")
    return {"total": len(results), "books": results}


@router.post("/borrow", tags=["Borrowing"])
async def borrow_book(request: BorrowRequest):
    user = find_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    book = find_book(request.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    if book["available_copies"] < 1:
        raise HTTPException(status_code=400, detail="No copies available.")

    for record in borrow_records_db:
        if record["user_id"] == request.user_id and record["book_id"] == request.book_id and not record["returned"]:
            raise HTTPException(
                status_code=400, detail="You already borrowed this book.")

    await asyncio.sleep(0)

    borrow_date = datetime.today().strftime("%Y-%m-%d")
    due_date = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")

    new_record = {
        "record_id": models.record_counter,
        "user_id": request.user_id,
        "book_id": request.book_id,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "returned": False,
        "fine": 0.0
    }

    borrow_records_db.append(new_record)
    book["available_copies"] -= 1
    models.record_counter += 1

    return {"message": f"'{book['title']}' borrowed by {user['name']}.", "record": new_record}


@router.put("/return", tags=["Borrowing"])
async def return_book(request: ReturnRequest):
    active_record = None
    for record in borrow_records_db:
        if record["user_id"] == request.user_id and record["book_id"] == request.book_id and not record["returned"]:
            active_record = record
            break

    if not active_record:
        raise HTTPException(
            status_code=404, detail="No active borrow record found.")

    await asyncio.sleep(0)

    fine = calculate_fine(active_record["due_date"])
    active_record["returned"] = True
    active_record["fine"] = fine

    book = find_book(request.book_id)
    if book:
        book["available_copies"] += 1

    user = find_user(request.user_id)

    return {
        "message": f"Book returned by {user['name']}.",
        "fine_charged": f"${fine}" if fine > 0 else "No fine — returned on time.",
        "record": active_record
    }


@router.get("/overdue", tags=["Fines & Overdue"])
async def get_overdue_books():
    today = datetime.today().strftime("%Y-%m-%d")
    overdue_list = []

    for record in borrow_records_db:
        if not record["returned"] and record["due_date"] < today:
            fine = calculate_fine(record["due_date"])
            record["fine"] = fine
            user = find_user(record["user_id"])
            book = find_book(record["book_id"])
            overdue_list.append({
                "record_id": record["record_id"],
                "user_name": user["name"] if user else "Unknown",
                "book_title": book["title"] if book else "Unknown",
                "due_date": record["due_date"],
                "fine": f"${fine}"
            })

    if not overdue_list:
        return {"message": "No overdue books at the moment.", "overdue": []}

    return {"total_overdue": len(overdue_list), "overdue": overdue_list}


@router.get("/users/{user_id}/history", tags=["Users"])
async def get_user_history(user_id: int):
    user = find_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    history = [r for r in borrow_records_db if r["user_id"] == user_id]
    return {"user": user["name"], "total_records": len(history), "history": history}


@router.post("/users", tags=["Users"])
async def register_user(user: User):
    if find_user(user.id):
        raise HTTPException(status_code=400, detail="User ID already exists.")
    users_db.append(user.dict())
    return {"message": f"User '{user.name}' registered successfully.", "user": user}


async def simulate_borrow(user_id: int, book_id: int) -> str:
    await asyncio.sleep(0.1)
    user = find_user(user_id)
    book = find_book(book_id)
    if user and book and book["available_copies"] > 0:
        return f"{user['name']} successfully borrowed '{book['title']}'"
    return f"User {user_id} could not borrow book {book_id}"


@router.get("/demo/concurrent-borrow", tags=["Demo"])
async def concurrent_borrow_demo():
    tasks = [
        simulate_borrow(1, 3),
        simulate_borrow(2, 4),
        simulate_borrow(3, 1),
    ]
    results = await asyncio.gather(*tasks)
    return {"message": "Concurrent borrowing simulation complete.", "results": list(results)}
