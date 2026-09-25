from pydantic_settings import BaseSettings, SettingsConfigDict


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

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
