from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas, security

router = APIRouter()

@router.post("/", response_model=schemas.ProjetoInvestimento)
def create_projeto_investimento_for_empresa(
    empresa_id: int,
    projeto: schemas.ProjetoInvestimentoCreate,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")
    return crud.create_projeto_investimento(db=db, projeto=projeto, empresa_id=empresa_id)

@router.get("/", response_model=List[schemas.ProjetoInvestimento])
def read_projetos_for_empresa(
    empresa_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")
    projetos = crud.get_projetos_by_empresa(db, empresa_id=empresa_id, skip=skip, limit=limit)
    return projetos

@router.get("/{projeto_id}", response_model=schemas.ProjetoInvestimento)
def read_projeto(
    empresa_id: int,
    projeto_id: int,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")

    db_projeto = crud.get_projeto(db, projeto_id=projeto_id)
    if db_projeto is None or db_projeto.empresa_id != empresa_id:
        raise HTTPException(status_code=404, detail="Projeto not found")

    return db_projeto

@router.put("/{projeto_id}", response_model=schemas.ProjetoInvestimento)
def update_projeto(
    empresa_id: int,
    projeto_id: int,
    projeto: schemas.ProjetoInvestimentoCreate,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")

    db_projeto = crud.get_projeto(db, projeto_id=projeto_id)
    if db_projeto is None or db_projeto.empresa_id != empresa_id:
        raise HTTPException(status_code=404, detail="Projeto not found")

    return crud.update_projeto(db=db, projeto_id=projeto_id, projeto=projeto)

@router.delete("/{projeto_id}", response_model=schemas.ProjetoInvestimento)
def delete_projeto(
    empresa_id: int,
    projeto_id: int,
    db: Session = Depends(security.get_db),
    current_user: models.Usuario = Depends(security.get_current_user)
):
    db_empresa = crud.get_empresa(db, empresa_id=empresa_id, user_id=current_user.id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa not found")

    db_projeto = crud.get_projeto(db, projeto_id=projeto_id)
    if db_projeto is None or db_projeto.empresa_id != empresa_id:
        raise HTTPException(status_code=404, detail="Projeto not found")

    return crud.delete_projeto(db=db, projeto_id=projeto_id)
