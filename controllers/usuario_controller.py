
from fastapi import HTTPException
from sqlmodel import Session, select

from models.cliente_model import Usuario


def buscar_usuario_por_email(
    db: Session,
    email: str
) -> Usuario:
    usuario = db.exec(
        select(Usuario).where(Usuario.email == email)
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    return usuario


def autenticar_usuario(
    db: Session,
    email: str,
    senha: str
) -> Usuario:
    usuario = buscar_usuario_por_email(
        db,
        email
    )

    if not usuario.ativo:
        raise HTTPException(
            status_code=403,
            detail="Este usuário está desativado."
        )

    if senha != usuario.senha_hash:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    return usuario
