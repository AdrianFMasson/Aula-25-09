from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel

from dependencies.dependencies import database
from routes.rota_cliente import cliente_rota


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Abre o túnel SSH, conecta no MySQL e garante que a tabela "clientes" exista
    engine = database.get_engine()
    SQLModel.metadata.create_all(engine)
    yield
    # Encerra o túnel SSH ao desligar a aplicação
    database.close_tunnel()


app = FastAPI(
    title="Cadastro de Clientes",
    description="API para cadastro de clientes, com FastAPI, SQLModel e MySQL via túnel SSH",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(cliente_rota)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/config")
def config():
    return {"mensagem": "Configuração carregada com sucesso a partir do .env"}
