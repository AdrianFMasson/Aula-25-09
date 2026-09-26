from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from routes.rota_cliente import clientes_rota

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(clientes_rota, prefix="/api")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )