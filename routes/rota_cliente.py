from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from controllers.cliente_controller import (
    atualizar_cliente,
    buscar_cliente,
    cadastrar_cliente,
    deletar_cliente,
    listar_clientes,
)
from dependencies.dependencies import database
from models.cliente_model import ClienteCreate, ClienteRead


cliente_rota = APIRouter(prefix="/api/clientes", tags=["Clientes"])


@cliente_rota.get("", response_model=List[ClienteRead])
def listar(s: Session = Depends(database.get_db)):
    return listar_clientes(s)


@cliente_rota.get("/{id_cliente}", response_model=ClienteRead)
def buscar(id_cliente: int, s: Session = Depends(database.get_db)):
    return buscar_cliente(s, id_cliente)


@cliente_rota.post("", response_model=ClienteRead, status_code=201)
def cadastrar(dados: ClienteCreate, s: Session = Depends(database.get_db)):
    try:
        return cadastrar_cliente(s, dados)
    except Exception as erro:
        s.rollback()
        raise HTTPException(
            status_code=500,
            detail="Não foi possível cadastrar o cliente."
        ) from erro


@cliente_rota.put("/{id_cliente}", response_model=ClienteRead)
def atualizar(
    id_cliente: int,
    dados: ClienteCreate,
    s: Session = Depends(database.get_db)
):
    return atualizar_cliente(s, id_cliente, dados)


@cliente_rota.delete("/{id_cliente}")
def deletar(id_cliente: int, s: Session = Depends(database.get_db)):
    return deletar_cliente(s, id_cliente)
