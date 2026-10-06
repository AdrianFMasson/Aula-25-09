CADASTRO DE CLIENTES - FASTAPI + SQLMODEL + MYSQL VIA TÚNEL SSH

EXECUÇÃO
1. Abra o terminal na pasta app.
2. Instale as dependências:
   py -m pip install -r requirements.txt
3. Inicie a API:
   py -m uvicorn main:app --host 127.0.0.1 --port 8000

Acesse a tela pelo navegador:
   http://127.0.0.1:8000

Swagger:
   http://127.0.0.1:8000/docs

ROTAS
GET    /api/clientes
GET    /api/clientes/{id}
POST   /api/clientes
PUT    /api/clientes/{id}
DELETE /api/clientes/{id}

IMPORTANTE
Não abra templates/index.html diretamente pelo Explorer.
A página deve ser aberta por http://127.0.0.1:8000, pois o próprio FastAPI entrega o HTML
e o JavaScript usa a rota relativa /api/clientes.

CONEXÃO
A aplicação usa FastAPI + SQLModel + SQLAlchemy + PyMySQL.
O acesso ao MySQL é feito pelo túnel SSH configurado no .env.

O arquivo app.py antigo, que misturava Flask com FastAPI, foi removido.
A pasta .venv e o repositório .git também não fazem parte do projeto final.
