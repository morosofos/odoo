from fastapi import FastAPI
from .database import engine, Base
from .routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to CRM Anormal"}
