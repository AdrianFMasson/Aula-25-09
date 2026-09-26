import logging
from urllib.parse import quote_plus

import sshtunnel
from sshtunnel import SSHTunnelForwarder
from sqlmodel import Session, create_engine

from config.Config import settings


sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


class Database:
    """Gerencia o túnel SSH e a engine SQLModel/SQLAlchemy."""

    def __init__(self):
        self._tunnel: SSHTunnelForwarder | None = None
        self._engine = None

    def _get_tunnel(self) -> SSHTunnelForwarder:
        if self._tunnel is None or not self._tunnel.is_active:
            self._tunnel = SSHTunnelForwarder(
                (settings.SSH_HOST, settings.SSH_PORT),
                ssh_username=settings.SSH_USER,
                ssh_password=settings.SSH_PASSWORD,
                remote_bind_address=("127.0.0.1", settings.DB_PORT),
                local_bind_address=("127.0.0.1", 3307),
            )

            try:
                self._tunnel.start()
                logging.info(
                    "Túnel SSH conectado com sucesso. Porta local: %s",
                    self._tunnel.local_bind_port,
                )
            except Exception:
                logging.exception("Erro ao iniciar o túnel SSH.")
                self._tunnel = None
                raise

        return self._tunnel

    def get_engine(self):
        if self._engine is None:
            tunnel = self._get_tunnel()
            senha_segura = quote_plus(settings.DB_PASSWORD)

            url = (
                f"mysql+pymysql://{settings.DB_USER}:{senha_segura}"
                f"@127.0.0.1:{tunnel.local_bind_port}/{settings.DB_NAME}"
            )

            self._engine = create_engine(
                url,
                echo=False,
                pool_pre_ping=True,
            )

            logging.info("Engine MySQL criada através do túnel SSH.")

        return self._engine

    def get_db(self):
        engine = self.get_engine()
        with Session(engine) as session:
            yield session

    def close_tunnel(self):
        if self._tunnel is not None:
            if self._tunnel.is_active:
                self._tunnel.stop()
            self._tunnel = None

        self._engine = None
        logging.info("Túnel SSH encerrado.")


database = Database()
