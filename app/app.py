import atexit

from flask import Flask, render_template
from dotenv import load_dotenv

from routes.cliente_routes import cliente_bp
from models.cliente_model import criar_tabela, encerrar_tunel

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Registro das rotas via Blueprint
app.register_blueprint(cliente_bp)

# Garante que o túnel SSH seja encerrado quando o processo do Flask for finalizado
atexit.register(encerrar_tunel)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    try:
        criar_tabela()
        print('Túnel SSH conectado e tabela "clientes" verificada/criada com sucesso.')
    except Exception as e:
        print(f'Aviso: não foi possível conectar ao banco de dados (via túnel SSH) na inicialização: {e}')

    # use_reloader=False evita que o Flask suba um segundo processo (comum no modo
    # debug), o que abriria um túnel SSH duplicado e pode gerar erro de porta em uso.
    app.run(debug=True, use_reloader=False)
