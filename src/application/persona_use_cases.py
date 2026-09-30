# src/application/persona_use_cases.py
from typing import List, Optional
from src.domain.entities import Persona
from src.domain.ports import PersonaRepositoryPort

class PersonaUseCases:
    def __init__(self, repository: PersonaRepositoryPort):
        self.repository = repository

    def crear_persona(
        self, 
        nombre: str, 
        apellido: str, 
        edad: int, 
        correo: str, 
        created_by: Optional[str] = None
    ) -> Persona:
        persona = Persona(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            correo=correo,
            created_by=created_by
        )
        return self.repository.save(persona)

    def obtener_persona(self, persona_id: int) -> Optional[Persona]:
        return self.repository.get_by_id(persona_id)

    def listar_personas(self) -> List[Persona]:
        return self.repository.get_all()

    def eliminar_persona(self, persona_id: int, deleted_by: Optional[str] = None) -> bool:
        return self.repository.delete(persona_id, deleted_by=deleted_by)