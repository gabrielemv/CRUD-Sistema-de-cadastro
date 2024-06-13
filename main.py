from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Cliente, Base
from schemas import ClienteCreate, Cliente as ClienteSchema
from database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Operations

# Create
@app.post("/clientes/", response_model=ClienteSchema)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = Cliente(nome=cliente.nome, email=cliente.email, telefone=cliente.telefone)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Read
@app.get("/clientes/", response_model=List[ClienteSchema])
def list_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@app.get("/clientes/{cliente_id}", response_model=ClienteSchema)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

# Update
@app.put("/clientes/{cliente_id}", response_model=ClienteSchema)
def update_cliente(cliente_id: int, updated_cliente: ClienteCreate, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    cliente.nome = updated_cliente.nome
    cliente.email = updated_cliente.email
    cliente.telefone = updated_cliente.telefone
    
    db.commit()
    db.refresh(cliente)
    return cliente

# Delete
@app.delete("/clientes/{cliente_id}", response_model=ClienteSchema)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(cliente)
    db.commit()
    return cliente
