from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FinAccess API"
    app_version: str = "0.1.0"
    secret_key: str = "CHANGE_THIS_IN_ENV"
    access_token_expire_minutes: int = 60

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/finaccess"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
