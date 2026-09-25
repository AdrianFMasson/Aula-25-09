import os
import pymysql
from sshtunnel import SSHTunnelForwarder

# Túnel SSH único, reaproveitado por toda a aplicação (evita abrir uma
# conexão SSH nova a cada requisição, o que seria lento e instável).
_tunnel = None


def _get_tunnel():
    """Garante que o túnel SSH esteja ativo e retorna a instância dele."""
    global _tunnel

    if _tunnel is None or not _tunnel.is_active:
        _tunnel = SSHTunnelForwarder(
            (os.getenv('SSH_HOST'), int(os.getenv('SSH_PORT', 22))),
            ssh_username=os.getenv('SSH_USER'),
            ssh_password=os.getenv('SSH_PASSWORD'),
            remote_bind_address=(
                os.getenv('DB_HOST', '127.0.0.1'),
                int(os.getenv('DB_PORT', 3306))
            )
        )
        _tunnel.start()

    return _tunnel


def encerrar_tunel():
    """Encerra o túnel SSH, se estiver ativo. Chamado no shutdown do Flask."""
    global _tunnel
    if _tunnel is not None and _tunnel.is_active:
        _tunnel.stop()
        _tunnel = None


def get_connection():
    """
    Abre o túnel SSH (se necessário) e retorna uma conexão MySQL via PyMySQL
    apontando para a porta local que o túnel expõe.
    """
    tunnel = _get_tunnel()

    return pymysql.connect(
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10
    )


def criar_tabela():
    """Cria a tabela de clientes caso ela ainda não exista."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(150) NOT NULL,
                    email VARCHAR(150) NOT NULL,
                    telefone VARCHAR(20) NOT NULL,
                    cidade VARCHAR(100) NOT NULL
                )
            ''')
        conn.commit()
    finally:
        conn.close()


def listar_clientes():
    """Retorna todos os clientes cadastrados, do mais recente para o mais antigo."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nome, email, telefone, cidade FROM clientes ORDER BY id DESC")
            return cursor.fetchall()
    finally:
        conn.close()


def buscar_cliente_por_id(id_cliente):
    """Busca um único cliente pelo ID."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, nome, email, telefone, cidade FROM clientes WHERE id = %s",
                (id_cliente,)
            )
            return cursor.fetchone()
    finally:
        conn.close()


def inserir_cliente(nome, email, telefone, cidade):
    """Insere um novo cliente e retorna o ID gerado."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO clientes (nome, email, telefone, cidade) VALUES (%s, %s, %s, %s)",
                (nome, email, telefone, cidade)
            )
            novo_id = cursor.lastrowid
        conn.commit()
        return novo_id
    finally:
        conn.close()


def atualizar_cliente(id_cliente, nome, email, telefone, cidade):
    """Atualiza os dados de um cliente existente. Retorna o número de linhas afetadas."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE clientes SET nome=%s, email=%s, telefone=%s, cidade=%s WHERE id=%s",
                (nome, email, telefone, cidade, id_cliente)
            )
            linhas_afetadas = cursor.rowcount
        conn.commit()
        return linhas_afetadas
    finally:
        conn.close()


def deletar_cliente(id_cliente):
    """Remove um cliente pelo ID. Retorna o número de linhas afetadas."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM clientes WHERE id=%s", (id_cliente,))
            linhas_afetadas = cursor.rowcount
        conn.commit()
        return linhas_afetadas
    finally:
        conn.close()
