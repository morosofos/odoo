from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, empresas, contatos, projetos

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(empresas.router, prefix="/empresas", tags=["empresas"])
app.include_router(contatos.router, prefix="/empresas/{empresa_id}/contatos", tags=["contatos"])
app.include_router(projetos.router, prefix="/empresas/{empresa_id}/projetos", tags=["projetos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to CRM Anormal"}
