# main.py
from fastapi import FastAPI
from src.infrastructure.database import init_db
from src.infrastructure.api.persona_router import router as persona_router

app = FastAPI(title="API Hexagonal con Auditoría - Persona", version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(persona_router)