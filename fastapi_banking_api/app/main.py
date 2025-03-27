from fastapi import FastAPI
from app.routes import transactions, users

app = FastAPI(title="API Bancária Assíncrona", version="1.0")

app.include_router(transactions.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Bancária!"}
