CADASTRO DE CLIENTES - FASTAPI + SQLMODEL + MYSQL VIA TÚNEL SSH

EXECUÇÃO
1. Abra o terminal na pasta app (a que contém main.py).
2. Instale as dependências:
   py -m pip install -r requirements.txt
3. Inicie a API:
   py -m uvicorn main:app --host 127.0.0.1 --port 8000

Acesse:
   http://127.0.0.1:8000

Swagger:
   http://127.0.0.1:8000/docs

ROTAS
GET    /api/clientes
GET    /api/clientes/{id}
POST   /api/clientes
PUT    /api/clientes/{id}
DELETE /api/clientes/{id}

CONEXÃO
A aplicação usa FastAPI + SQLModel + SQLAlchemy + PyMySQL.
O acesso ao MySQL é feito exclusivamente pelo túnel SSH configurado em .env,
seguindo o mesmo método usado no MySQL Workbench: SSH -> MySQL 127.0.0.1:3306.

Não use --reload durante o teste do túnel, pois o processo extra pode abrir
outro túnel SSH.
