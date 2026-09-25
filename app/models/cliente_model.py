from typing import Optional
from sqlmodel import SQLModel, Field


class Cliente(SQLModel, table=True):
    """Tabela `clientes` no MySQL."""

    __tablename__ = "clientes"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=150)
    email: str = Field(max_length=150)
    telefone: str = Field(max_length=20)
    cidade: str = Field(max_length=100)


class ClienteCreate(SQLModel):
    """Schema de entrada para criação/atualização de cliente."""

    nome: str
    email: str
    telefone: str
    cidade: str


class ClienteRead(SQLModel):
    """Schema de saída (o que a API devolve)."""

    id: int
    nome: str
    email: str
    telefone: str
    cidade: str
