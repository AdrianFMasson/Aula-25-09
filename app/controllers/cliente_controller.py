from typing import Sequence

from fastapi import HTTPException
from sqlmodel import Session, select

from models.cliente_model import Cliente, ClienteCreate


def listar_clientes(db: Session) -> Sequence[Cliente]:
    return db.exec(select(Cliente).order_by(Cliente.id.desc())).all()


def buscar_cliente(db: Session, id_cliente: int) -> Cliente:
    cliente = db.get(Cliente, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente


def cadastrar_cliente(db: Session, dados: ClienteCreate) -> Cliente:
    cliente = Cliente(**dados.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def atualizar_cliente(db: Session, id_cliente: int, dados: ClienteCreate) -> Cliente:
    cliente = buscar_cliente(db, id_cliente)
    for campo, valor in dados.model_dump().items():
        setattr(cliente, campo, valor)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def deletar_cliente(db: Session, id_cliente: int) -> dict:
    cliente = buscar_cliente(db, id_cliente)
    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente removido com sucesso."}
