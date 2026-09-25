from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from dependencies.dependencies import database
from models.cliente_model import Cliente, ClienteCreate, ClienteRead

cliente_rota = APIRouter(prefix="/api/clientes", tags=["Clientes"])


@cliente_rota.get("", response_model=List[ClienteRead])
def listar_clientes(s: Session = Depends(database.get_db)):
    """GET - lista todos os clientes, do mais recente para o mais antigo."""
    resultado = s.exec(select(Cliente).order_by(Cliente.id.desc())).all()
    return resultado


@cliente_rota.get("/{id_cliente}", response_model=ClienteRead)
def buscar_cliente(id_cliente: int, s: Session = Depends(database.get_db)):
    """GET - busca um único cliente pelo ID."""
    cliente = s.get(Cliente, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente


@cliente_rota.post("", response_model=ClienteRead, status_code=201)
def cadastrar_cliente(dados: ClienteCreate, s: Session = Depends(database.get_db)):
    """POST - cadastra um novo cliente."""
    cliente = Cliente(**dados.model_dump())
    s.add(cliente)
    s.commit()
    s.refresh(cliente)
    return cliente


@cliente_rota.put("/{id_cliente}", response_model=ClienteRead)
def atualizar_cliente(id_cliente: int, dados: ClienteCreate, s: Session = Depends(database.get_db)):
    """PUT - atualiza os dados de um cliente existente pelo ID."""
    cliente = s.get(Cliente, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    cliente.nome = dados.nome
    cliente.email = dados.email
    cliente.telefone = dados.telefone
    cliente.cidade = dados.cidade

    s.add(cliente)
    s.commit()
    s.refresh(cliente)
    return cliente


@cliente_rota.delete("/{id_cliente}")
def deletar_cliente(id_cliente: int, s: Session = Depends(database.get_db)):
    """DELETE - remove um cliente pelo ID."""
    cliente = s.get(Cliente, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    s.delete(cliente)
    s.commit()
    return {"mensagem": "Cliente removido com sucesso."}
