from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, TIMESTAMP, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hash_senha = Column(String(255), nullable=False)
    e_supervisor = Column(Boolean, default=False, nullable=False)

    empresas = relationship("Empresa", back_populates="usuario_responsavel")

class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True)
    nome_fantasia = Column(String(255), nullable=False)
    razao_social = Column(String(255))
    cnpj = Column(String(14), unique=True)
    situacao = Column(String(50), nullable=False, default='Prospecção')
    usuario_responsavel_id = Column(Integer, ForeignKey('usuario.id'), nullable=True)
    data_criacao = Column(TIMESTAMP(timezone=True), server_default=func.now())
    data_ultima_alteracao = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    usuario_responsavel = relationship("Usuario", back_populates="empresas")
    contatos = relationship("Contato", back_populates="empresa")

class Contato(Base):
    __tablename__ = "contato"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cargo = Column(String(100))
    email = Column(String(255))
    telefone = Column(String(50))
    empresa_id = Column(Integer, ForeignKey('empresa.id'), nullable=False)
    observacao = Column(TEXT)

    empresa = relationship("Empresa", back_populates="contatos")
