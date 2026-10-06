import logging
from urllib.parse import quote_plus

from sshtunnel import SSHTunnelForwarder
from sqlmodel import Session, create_engine
from sqlalchemy import text

from config.Config import settings


class Database:

    def __init__(self):
        self._tunnel = None
        self._engine = None

    def _get_tunnel(self):
        if self._tunnel is not None and self._tunnel.is_active:
            return self._tunnel

        if self._tunnel is not None:
            try:
                self._tunnel.stop()
            except Exception:
                logging.exception("Erro ao encerrar túnel SSH anterior.")
            self._tunnel = None

        logging.info(
            "Iniciando túnel SSH para %s:%s...",
            settings.SSH_HOST,
            settings.SSH_PORT
        )

        try:
            self._tunnel = SSHTunnelForwarder(
                (settings.SSH_HOST, settings.SSH_PORT),
                ssh_username=settings.SSH_USER,
                ssh_password=settings.SSH_PASSWORD,
                remote_bind_address=(
                    settings.DB_HOST,
                    settings.DB_PORT
                ),
                local_bind_address=(
                    "127.0.0.1",
                    0
                ),
                set_keepalive=30.0
            )

            self._tunnel.start()

            logging.info("Túnel SSH conectado.")

            logging.info(
                "MySQL remoto %s:%s disponível localmente em 127.0.0.1:%s",
                settings.DB_HOST,
                settings.DB_PORT,
                self._tunnel.local_bind_port
            )

            return self._tunnel

        except Exception:
            logging.exception(
                "Não foi possível iniciar o túnel SSH."
            )
            self._tunnel = None
            raise

    def get_engine(self):
        if (
            self._engine is not None
            and self._tunnel is not None
            and self._tunnel.is_active
        ):
            return self._engine

        if self._engine is not None:
            try:
                self._engine.dispose()
            except Exception:
                logging.exception(
                    "Erro ao descartar engine antiga."
                )

            self._engine = None

        tunnel = self._get_tunnel()

        senha_segura = quote_plus(settings.DB_PASSWORD)

        database_url = (
            f"mysql+pymysql://"
            f"{settings.DB_USER}:"
            f"{senha_segura}"
            f"@127.0.0.1:"
            f"{tunnel.local_bind_port}/"
            f"{settings.DB_NAME}"
            f"?charset=utf8mb4"
        )

        logging.info(
            "Criando engine MySQL através do túnel SSH."
        )

        self._engine = create_engine(
            database_url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_size=5,
            max_overflow=10,
            connect_args={
                "connect_timeout": 10
            }
        )

        return self._engine

    def get_db(self):
        engine = self.get_engine()

        with Session(engine) as session:
            try:
                yield session
            except Exception:
                session.rollback()
                raise

    def test_connection(self):
        try:
            engine = self.get_engine()

            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            logging.info(
                "Conexão com MySQL testada com sucesso."
            )

            return True

        except Exception:
            logging.exception(
                "Falha no teste de conexão com MySQL."
            )

            return False

    def close_tunnel(self):
        logging.info(
            "Encerrando conexão com banco de dados..."
        )

        if self._engine is not None:
            try:
                self._engine.dispose()
            except Exception:
                logging.exception(
                    "Erro ao encerrar engine."
                )

            self._engine = None

        if self._tunnel is not None:
            try:
                if self._tunnel.is_active:
                    self._tunnel.stop()
            except Exception:
                logging.exception(
                    "Erro ao encerrar túnel SSH."
                )
            finally:
                self._tunnel = None

        logging.info(
            "Conexão com banco encerrada."
        )


database = Database()