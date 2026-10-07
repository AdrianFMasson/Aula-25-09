from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from controllers.usuario_controller import autenticar_usuario
from dependencies.dependencies import database
from dependencies.autenticacao import (
    criar_token_sessao,
    obter_token_da_requisicao,
    validar_token_sessao,
    encerrar_sessao
)
from utils.validacao_senha import validar_senha


login_rota = APIRouter()

templates = Jinja2Templates(directory="templates")


@login_rota.get("/login")
def pagina_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@login_rota.post("/api/login")
def realizar_login(
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(database.get_db)
):
    if not validar_senha(senha):
        raise HTTPException(
            status_code=400,
            detail="A senha deve possuir no mínimo 6 caracteres, uma letra maiúscula, uma letra minúscula e um caractere especial."
        )

    usuario = autenticar_usuario(
        db,
        email,
        senha
    )

    token = criar_token_sessao(
        usuario.id_usuario
    )

    return {
        "mensagem": "Login realizado com sucesso.",
        "usuario": usuario.nome,
        "email": usuario.email,
        "token": token
    }


@login_rota.get("/api/verificar-login")
def verificar_login(request: Request):
    token = obter_token_da_requisicao(request)

    sessao = validar_token_sessao(token)

    return {
        "autenticado": True,
        "usuario_id": sessao["usuario_id"]
    }


@login_rota.post("/api/logout")
def realizar_logout(request: Request):
    token = request.headers.get("Authorization")

    if token and token.startswith("Bearer "):
        token = token[7:].strip()

        if token:
            encerrar_sessao(token)

    request.session.clear()

    return {
        "mensagem": "Sessão encerrada com sucesso."
    }