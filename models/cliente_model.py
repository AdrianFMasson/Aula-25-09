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
