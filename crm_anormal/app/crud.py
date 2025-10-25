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
