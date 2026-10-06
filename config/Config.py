import os

from pydantic_settings import BaseSettings, SettingsConfigDict

# Caminho absoluto até a raiz do projeto (uma pasta acima de config/),
# para que o .env seja encontrado não importa de onde o comando for executado.
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENV_PATH = os.path.join(_BASE_DIR, ".env")


class Settings(BaseSettings):
    """Configurações lidas do arquivo .env (túnel SSH + acesso ao MySQL)."""

    SSH_HOST: str
    SSH_PORT: int = 22
    SSH_USER: str
    SSH_PASSWORD: str

    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(env_file=_ENV_PATH, extra="ignore")


settings = Settings()
