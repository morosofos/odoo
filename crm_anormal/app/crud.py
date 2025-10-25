from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.Usuario(
        email=user.email,
        nome=user.nome,
        hash_senha=hashed_password,
        e_supervisor=user.e_supervisor
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Funções CRUD para Empresa
def create_empresa(db: Session, empresa: schemas.EmpresaCreate, user_id: int):
    db_empresa = models.Empresa(**empresa.dict(), usuario_responsavel_id=user_id)
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

def get_empresas(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Empresa).filter(models.Empresa.usuario_responsavel_id == user_id).offset(skip).limit(limit).all()

def get_empresa(db: Session, empresa_id: int, user_id: int):
    return db.query(models.Empresa).filter(models.Empresa.id == empresa_id, models.Empresa.usuario_responsavel_id == user_id).first()

def update_empresa(db: Session, empresa_id: int, empresa: schemas.EmpresaCreate):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if db_empresa:
        for key, value in empresa.dict().items():
            setattr(db_empresa, key, value)
        db.commit()
        db.refresh(db_empresa)
    return db_empresa

def delete_empresa(db: Session, empresa_id: int):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if db_empresa:
        db.delete(db_empresa)
        db.commit()
    return db_empresa

# Funções CRUD para Contato
def create_contato(db: Session, contato: schemas.ContatoCreate, empresa_id: int):
    db_contato = models.Contato(**contato.dict(), empresa_id=empresa_id)
    db.add(db_contato)
    db.commit()
    db.refresh(db_contato)
    return db_contato

def get_contatos_by_empresa(db: Session, empresa_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Contato).filter(models.Contato.empresa_id == empresa_id).offset(skip).limit(limit).all()

def get_contato(db: Session, contato_id: int):
    return db.query(models.Contato).filter(models.Contato.id == contato_id).first()

def update_contato(db: Session, contato_id: int, contato: schemas.ContatoCreate):
    db_contato = db.query(models.Contato).filter(models.Contato.id == contato_id).first()
    if db_contato:
        for key, value in contato.dict().items():
            setattr(db_contato, key, value)
        db.commit()
        db.refresh(db_contato)
    return db_contato

def delete_contato(db: Session, contato_id: int):
    db_contato = db.query(models.Contato).filter(models.Contato.id == contato_id).first()
    if db_contato:
        db.delete(db_contato)
        db.commit()
    return db_contato
