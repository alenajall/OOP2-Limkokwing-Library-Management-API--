# OOP2

Assignment 1
Alhaji Abubakarr Jalloh- Dit1201

# Limkokwing Library Management API

PROG315 – Object-Oriented Programming 2  
Limkokwing University of Creative Technology – Sierra Leone

## Description

A RESTful API built with Python FastAPI that digitally manages the Limkokwing University library. Users can search for books, borrow and return them, track overdue fines, and the system supports multiple concurrent users via async/await.

## Project Structure

```
project/
├── main.py        # Entry point
├── models.py      # OOP classes and sample data
├── routes.py      # API endpoints
├── README.md
└── .gitignore
```

## Installation

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint                   | Description                                |
| ------ | -------------------------- | ------------------------------------------ |
| GET    | `/books`                   | Search books by title, author, or category |
| POST   | `/borrow`                  | Borrow a book                              |
| PUT    | `/return`                  | Return a book                              |
| GET    | `/overdue`                 | View overdue books and fines               |
| GET    | `/users/{user_id}/history` | User borrowing history                     |
| POST   | `/users`                   | Register a new user                        |
| GET    | `/demo/concurrent-borrow`  | Async demo                                 |

## Docs

Visit `http://127.0.0.1:8000/docs` after running the server.

## SDG Alignment

SDG 4 – Quality Education: Digitizing library access improves availability of learning resources for students.
