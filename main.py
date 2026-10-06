from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routes.rota_cliente import cliente_rota

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="API de Clientes",
    description="API para cadastro e consulta de clientes",
    version="1.0.0"
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

app.mount(
    "/css",
    StaticFiles(directory=str(BASE_DIR / "css")),
    name="css"
)

app.include_router(cliente_rota)

@app.get("/")
def pagina_inicial(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )