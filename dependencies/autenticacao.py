import secrets

from fastapi import HTTPException, Request


sessoes_ativas = {}


def criar_token_sessao(usuario_id: int) -> str:
    token = secrets.token_urlsafe(64)

    sessoes_ativas[token] = {
        "usuario_id": usuario_id
    }

    return token


def validar_token_sessao(token: str):
    sessao = sessoes_ativas.get(token)

    if not sessao:
        raise HTTPException(
            status_code=401,
            detail="Sessão inválida ou expirada."
        )

    return sessao


def obter_token_da_requisicao(request: Request) -> str:
    autorizacao = request.headers.get("Authorization")

    if not autorizacao:
        raise HTTPException(
            status_code=401,
            detail="Token de sessão não informado."
        )

    if not autorizacao.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Token de sessão inválido."
        )

    token = autorizacao[7:].strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token de sessão não informado."
        )

    return token


def usuario_autenticado(request: Request) -> int:
    token = obter_token_da_requisicao(request)
    sessao = validar_token_sessao(token)

    return sessao["usuario_id"]


def encerrar_sessao(token: str):
    sessoes_ativas.pop(token, None)