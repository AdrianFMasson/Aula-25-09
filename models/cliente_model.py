from datetime import datetime
from sqlmodel import Field, SQLModel

class Cliente(SQLModel, table=True):
    """Tabela clientes no MySQL."""

    __tablename__ = "clientes"

    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    email: str = Field(max_length=150)
    telefone: str = Field(max_length=20)
    cidade: str = Field(max_length=100)


class ClienteCreate(SQLModel):
    """Dados aceitos para criação ou atualização de cliente."""

    nome: str
    email: str
    telefone: str
    cidade: str


class ClienteRead(SQLModel):
    """Dados devolvidos pela API."""

    id: int
    nome: str
    email: str
    telefone: str
    cidade: str

from datetime import datetime

from sqlmodel import Field, SQLModel


class Usuario(SQLModel, table=True):
    """Tabela de usuários para autenticação no MySQL."""

    __tablename__ = "login"

    id_usuario: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True)
    senha_hash: str = Field(max_length=255)
    nome: str = Field(max_length=100)
    ativo: bool = Field(default=True)
    dt_cadastro: datetime = Field(default_factory=datetime.now)


class UsuarioLogin(SQLModel):
    """Dados recebidos para realizar o login."""

    email: str
    senha: str