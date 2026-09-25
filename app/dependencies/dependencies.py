import sshtunnel
from sshtunnel import SSHTunnelForwarder
from sqlmodel import create_engine, Session

from config.Config import settings

# Evita que uma tentativa de conexão SSH sem resposta trave o servidor
# indefinidamente: se a rede/VPN não alcançar o SSH_HOST em 10s, a conexão
# falha com um erro claro em vez de ficar pendurada.
sshtunnel.SSH_TIMEOUT = 10.0
sshtunnel.TUNNEL_TIMEOUT = 10.0


class Database:
    """
    Gerencia o túnel SSH e a engine do SQLModel/SQLAlchemy.
    O túnel é aberto uma única vez e reaproveitado por toda a aplicação.
    """

    def __init__(self):
        self._tunnel: SSHTunnelForwarder | None = None
        self._engine = None

    def _get_tunnel(self) -> SSHTunnelForwarder:
        if self._tunnel is None or not self._tunnel.is_active:
            self._tunnel = SSHTunnelForwarder(
                (settings.SSH_HOST, settings.SSH_PORT),
                ssh_username=settings.SSH_USER,
                ssh_password=settings.SSH_PASSWORD,
                remote_bind_address=(settings.DB_HOST, settings.DB_PORT),
            )
            self._tunnel.start()
        return self._tunnel

    def get_engine(self):
        """Cria (se necessário) e retorna a engine do SQLModel apontando para o túnel."""
        if self._engine is None:
            tunnel = self._get_tunnel()
            url = (
                f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
                f"@127.0.0.1:{tunnel.local_bind_port}/{settings.DB_NAME}"
            )
            self._engine = create_engine(url, echo=False, pool_pre_ping=True)
        return self._engine

    def get_db(self):
        """Dependência do FastAPI: entrega uma Session por requisição."""
        engine = self.get_engine()
        with Session(engine) as session:
            yield session

    def close_tunnel(self):
        """Encerra o túnel SSH. Chamado no shutdown da aplicação (lifespan)."""
        if self._tunnel is not None and self._tunnel.is_active:
            self._tunnel.stop()
            self._tunnel = None
        self._engine = None


database = Database()
