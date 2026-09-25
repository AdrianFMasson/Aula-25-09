CADASTRO DE CLIENTES - FLASK MVC + MYSQL

ESTRUTURA:
Aula-25-09/
  app.py
  .env
  banco.sql
  requirements.txt
  models/cliente_model.py
  controllers/cliente_controller.py
  routes/cliente_routes.py
  templates/index.html
  static/css/style.css

INSTALAÇÃO:
1. Abra o terminal na pasta do projeto.
2. Execute:
   py -m pip install -r requirements.txt

BANCO:
Execute banco.sql no MySQL.

EXECUÇÃO:
py app.py

Acesse:
http://127.0.0.1:5000

ROTAS:
GET    /api/clientes
GET    /api/clientes/<id>
POST   /api/clientes
PUT    /api/clientes/<id>
DELETE /api/clientes/<id>

O formulário usa POST via fetch() e a tabela é atualizada sem recarregar
a página. O campo seguinte é liberado conforme o anterior é preenchido.
