import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel

from dependencies.dependencies import database
from routes.rota_cliente import cliente_rota

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Abre a conexão pelo túnel SSH e cria as tabelas necessárias."""

    engine = database.get_engine()
    SQLModel.metadata.create_all(engine)

    try:
        yield
    finally:
        database.close_tunnel()


app = FastAPI(
    title="Cadastro de Clientes",
    description="API para cadastro de clientes com FastAPI, SQLModel e MySQL via túnel SSH.",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "css")),
    name="static",
)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)

app.include_router(cliente_rota)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.get("/config")
def config():
    return {"mensagem": "Configuração carregada com sucesso a partir do .env"}
