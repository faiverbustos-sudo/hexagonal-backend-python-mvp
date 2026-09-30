# src/infrastructure/api/persona_router.py
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from src.application.persona_use_cases import PersonaUseCases
from src.infrastructure.database import get_db
from src.infrastructure.adapters.sqlserver_persona_repository import SqlServerPersonaRepository

router = APIRouter(prefix="/personas", tags=["Personas"])

class PersonaCreateRequest(BaseModel):
    nombre: str
    apellido: str
    edad: int
    correo: EmailStr

class PersonaResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int
    correo: EmailStr
    created_date: datetime
    created_by: Optional[str] = None
    modified_date: Optional[datetime] = None
    modified_by: Optional[str] = None
    is_deleted: bool

def get_use_case() -> PersonaUseCases:
    # Usando el repositorio directo de SQL Server con pyodbc
    repo = SqlServerPersonaRepository()
    return PersonaUseCases(repo)

@router.post("/", response_model=PersonaResponse, status_code=201)
def crear_persona(
    payload: PersonaCreateRequest, 
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    use_case: PersonaUseCases = Depends(get_use_case)
):
    persona = use_case.crear_persona(
        nombre=payload.nombre,
        apellido=payload.apellido,
        edad=payload.edad,
        correo=payload.correo,
        created_by=x_user_id
    )
    return persona

@router.get("/{persona_id}", response_model=PersonaResponse)
def obtener_persona(persona_id: int, use_case: PersonaUseCases = Depends(get_use_case)):
    persona = use_case.obtener_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@router.get("/", response_model=List[PersonaResponse])
def listar_personas(use_case: PersonaUseCases = Depends(get_use_case)):
    return use_case.listar_personas()

@router.delete("/{persona_id}", status_code=204)
def eliminar_persona(
    persona_id: int,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
    use_case: PersonaUseCases = Depends(get_use_case)
):
    exito = use_case.eliminar_persona(persona_id, deleted_by=x_user_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Persona no encontrada o ya eliminada")
    return None