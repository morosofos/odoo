from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas, security

router = APIRouter()

@router.post("/", response_model=schemas.Contato)
def create_contato_for_empresa(
    empresa_id: int,
    contato: schemas.ContatoCreate,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")

    return crud.create_contato(db=db, contato=contato, empresa_id=empresa_id)

@router.get("/", response_model=List[schemas.Contato])
def read_contatos_for_empresa(
    empresa_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")

    contatos = crud.get_contatos_by_empresa(db, empresa_id=empresa_id, skip=skip, limit=limit)
    return contatos

@router.put("/{contato_id}", response_model=schemas.Contato)
def update_contato(
    empresa_id: int,
    contato_id: int,
    contato: schemas.ContatoCreate,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")

    db_contato = crud.get_contato(db, contato_id=contato_id)
    if db_contato is None or db_contato.empresa_id != empresa_id:
        raise HTTPException(status_code=404, detail="Contato not found")

    return crud.update_contato(db=db, contato_id=contato_id, contato=contato)

@router.delete("/{contato_id}", response_model=schemas.Contato)
def delete_contato(
    empresa_id: int,
    contato_id: int,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")

    db_contato = crud.get_contato(db, contato_id=contato_id)
    if db_contato is None or db_contato.empresa_id != empresa_id:
        raise HTTPException(status_code=404, detail="Contato not found")

    return crud.delete_contato(db=db, contato_id=contato_id)
