from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Limkokwing Library Management API",
    description="A digital library system for Limkokwing University - Sierra Leone",
    version="1.0.0"
)

app.include_router(router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Limkokwing Library Management API",
        "version": "1.0.0",
        "docs": "http://127.0.0.1:8000/docs",
        "endpoints": [
            "GET  /books                   - Search books",
            "POST /borrow                  - Borrow a book",
            "PUT  /return                  - Return a book",
            "GET  /overdue                 - View overdue books and fines",
            "GET  /users/{user_id}/history - User borrowing history",
            "POST /users                   - Register a new user",
            "GET  /demo/concurrent-borrow  - Async demo"
        ]
    }
