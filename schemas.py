from pydantic import BaseModel
from typing import Optional

class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None

class Cliente(BaseModel):
    id: int
    nome: str
    email: str
    telefone: Optional[str] = None

    class Config:
        orm_mode = True
