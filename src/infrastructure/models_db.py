# src/infrastructure/models_db.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AuditableModel(Base):
    __abstract__ = True

    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(String(100), nullable=True)
    modified_date = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    modified_by = Column(String(100), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)

class PersonaModel(AuditableModel):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    edad = Column(Integer, nullable=False)
    correo = Column(String(100), unique=True, index=True, nullable=False)