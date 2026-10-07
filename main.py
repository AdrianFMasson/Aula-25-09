from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from routes.rota_login import login_rota
from routes.rota_cliente import cliente_rota


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="API de Clientes",
    description="API para cadastro e consulta de clientes",
    version="1.0.0"
)


app.add_middleware(
    SessionMiddleware,
    secret_key="chave-secreta-do-projeto"
)


app.include_router(login_rota)
app.include_router(cliente_rota)


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


app.mount(
    "/css",
    StaticFiles(directory=str(BASE_DIR / "css")),
    name="css"
)


@app.get("/")
def pagina_inicial(request: Request):
    response = templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0"
    )

    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response