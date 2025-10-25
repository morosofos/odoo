from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas, security

router = APIRouter()

@router.post("/", response_model=schemas.Empresa)
def create_empresa(
    empresa: schemas.EmpresaCreate,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    return crud.create_empresa(db=db, empresa=empresa, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Empresa])
def read_empresas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    empresas = crud.get_empresas(db, user_id=current_user.id, skip=skip, limit=limit)
    return empresas

@router.get("/{empresa_id}", response_model=schemas.Empresa)
def read_empresa(
    empresa_id: int,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")
    return db_empresa

@router.put("/{empresa_id}", response_model=schemas.Empresa)
def update_empresa(
    empresa_id: int,
    empresa: schemas.EmpresaCreate,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")
    return crud.update_empresa(db=db, empresa_id=empresa_id, empresa=empresa)

@router.delete("/{empresa_id}", response_model=schemas.Empresa)
def delete_empresa(
    empresa_id: int,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")
    return crud.delete_empresa(db=db, empresa_id=empresa_id)
