from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    nome: str
    email: str
    e_supervisor: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class ProjetoInvestimentoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    status: str = 'Análise'
    investimento_estimado_reais: Optional[Decimal] = None
    empregos_estimados_diretos: Optional[int] = None
    data_inicio_prevista: Optional[date] = None
    data_operacao_prevista: Optional[date] = None

class ProjetoInvestimentoCreate(ProjetoInvestimentoBase):
    pass

class ProjetoInvestimento(ProjetoInvestimentoBase):
    id: int
    empresa_id: int

    class Config:
        orm_mode = True

class ContatoBase(BaseModel):
    nome: str
    cargo: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    observacao: Optional[str] = None

class ContatoCreate(ContatoBase):
    pass

class Contato(ContatoBase):
    id: int
    empresa_id: int

    class Config:
        orm_mode = True

class EmpresaBase(BaseModel):
    nome_fantasia: str
    razao_social: Optional[str] = None
    cnpj: Optional[str] = None
    situacao: str = 'Prospecção'

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int
    usuario_responsavel_id: Optional[int] = None
    contatos: list[Contato] = []

    class Config:
        orm_mode = True
