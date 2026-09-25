CADASTRO DE CLIENTES - FASTAPI + SQLMODEL + MYSQL (via túnel SSH)

ESTRUTURA:
Aula-25-09/
  main.py
  .env
  requirements.txt
  config/
    Config.py
  dependencies/
    dependencies.py
  models/
    cliente_model.py
  routes/
    rota_cliente.py
  static/css/style.css
  templates/index.html

INSTALAÇÃO:
1. Abra o terminal na pasta do projeto (a que contém main.py).
2. Execute:
   py -m pip install -r requirements.txt

EXECUÇÃO:
   py -m uvicorn main:app --host 127.0.0.1 --port 8000

   IMPORTANTE: não use a flag --reload em produção/teste com o túnel SSH.
   O --reload sobe um processo extra do uvicorn e abriria dois túneis SSH
   ao mesmo tempo, o que pode travar ou dar erro de porta em uso.

Acesse:
   http://127.0.0.1:8000

Documentação automática da API (Swagger):
   http://127.0.0.1:8000/docs

ROTAS:
GET    /api/clientes
GET    /api/clientes/{id}
POST   /api/clientes
PUT    /api/clientes/{id}
DELETE /api/clientes/{id}

REDE / TÚNEL SSH:
A conexão com o MySQL depende de acesso ao servidor SSH (10.10.230.213).
Se estiver fora da rede/VPN da escola, a conexão falhará com um erro de
timeout claro no terminal (em vez de travar), pois SSH_TIMEOUT e
TUNNEL_TIMEOUT já estão configurados em dependencies/dependencies.py.

O formulário usa fetch() e a tabela é atualizada sem recarregar a página.
Cada campo é liberado conforme o anterior é preenchido (Nome -> E-mail ->
Telefone -> Cidade), e o telefone recebe máscara automática.
