# src/infrastructure/adapters/sqlserver_persona_repository.py
import pyodbc
from datetime import datetime
from typing import List, Optional
from src.domain.entities import Persona
from src.domain.ports import PersonaRepositoryPort

class SqlServerPersonaRepository(PersonaRepositoryPort):
    def __init__(self):
        # Cadena de conexión con mapeo exacto para pyodbc
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=WebApplication1;"
            "UID=WebApplication1;"
            "PWD=wa2026*;"
            "TrustServerCertificate=Yes;"
        )

    def _get_connection(self):
        return pyodbc.connect(self.connection_string)

    def _to_domain(self, row: pyodbc.Row) -> Persona:
        """Mapea una fila de SQL Server (PascalCase) a la entidad de Dominio en Python."""
        return Persona(
            id=row.Id,
            nombre=row.Nombre,
            apellido=row.Apellido,
            edad=row.Edad,
            correo=row.Correo,
            created_by=row.CreatedBy,
            created_date=row.CreatedDate,
            is_deleted=bool(row.IsDeleted),
            modified_by=row.ModifiedBy,
            modified_date=row.ModifiedDate
        )

    def save(self, persona: Persona) -> Persona:
        now = datetime.utcnow()
        created_date = persona.created_date or now
        
        sql = """
            INSERT INTO [WebApplication1].[dbo].[Personas]
                ([Nombre], [Apellido], [Edad], [Correo], [CreatedBy], [CreatedDate], [IsDeleted])
            OUTPUT INSERTED.Id
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (
                persona.nombre,
                persona.apellido,
                persona.edad,
                persona.correo,
                persona.created_by,
                created_date,
                1 if persona.is_deleted else 0
            ))
            persona.id = cursor.fetchone()[0]
            persona.created_date = created_date
            conn.commit()
            return persona

    def get_by_id(self, persona_id: int) -> Optional[Persona]:
        sql = """
            SELECT [Id], [Nombre], [Apellido], [Edad], [Correo], 
                   [CreatedBy], [CreatedDate], [IsDeleted], [ModifiedBy], [ModifiedDate]
            FROM [WebApplication1].[dbo].[Personas]
            WHERE [Id] = ? AND [IsDeleted] = 0;
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (persona_id,))
            row = cursor.fetchone()
            return self._to_domain(row) if row else None

    def get_all(self) -> List[Persona]:
        sql = """
            SELECT [Id], [Nombre], [Apellido], [Edad], [Correo], 
                   [CreatedBy], [CreatedDate], [IsDeleted], [ModifiedBy], [ModifiedDate]
            FROM [WebApplication1].[dbo].[Personas]
            WHERE [IsDeleted] = 0;
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [self._to_domain(row) for row in rows]

    def update(self, persona: Persona) -> Persona:
        modified_date = datetime.utcnow()
        sql = """
            UPDATE [WebApplication1].[dbo].[Personas]
            SET [Nombre] = ?, 
                [Apellido] = ?, 
                [Edad] = ?, 
                [Correo] = ?, 
                [ModifiedBy] = ?, 
                [ModifiedDate] = ?
            WHERE [Id] = ? AND [IsDeleted] = 0;
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (
                persona.nombre,
                persona.apellido,
                persona.edad,
                persona.correo,
                persona.modified_by,
                modified_date,
                persona.id
            ))
            conn.commit()
            persona.modified_date = modified_date
            return persona

    def delete(self, persona_id: int, deleted_by: Optional[str] = None) -> bool:
        modified_date = datetime.utcnow()
        sql = """
            UPDATE [WebApplication1].[dbo].[Personas]
            SET [IsDeleted] = 1, 
                [ModifiedBy] = ?, 
                [ModifiedDate] = ?
            WHERE [Id] = ? AND [IsDeleted] = 0;
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (deleted_by, modified_date, persona_id))
            conn.commit()
            return cursor.rowcount > 0