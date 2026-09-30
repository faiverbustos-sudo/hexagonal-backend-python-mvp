# src/domain/entities.py
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class AuditableEntity:
    created_date: datetime = field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    modified_date: Optional[datetime] = None
    modified_by: Optional[str] = None
    is_deleted: bool = False

@dataclass
class Persona(AuditableEntity):
    nombre: str = ""
    apellido: str = ""
    edad: int = 0
    correo: str = ""
    id: Optional[int] = None