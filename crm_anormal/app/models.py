from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hash_senha = Column(String(255), nullable=False)
    e_supervisor = Column(Boolean, default=False, nullable=False)
