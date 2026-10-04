import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_env: str
    api_timeout: int
    secret_key: str

    @classmethod
    def load(cls) -> "Settings":
        app_env = os.getenv("APP_ENV", "development")

        raw_timeout = os.getenv("API_TIMEOUT", "30")
        try:
            api_timeout = int(raw_timeout)
        except ValueError:
            raise ValueError(f"API_TIMEOUT must be an integer, got: {raw_timeout}")

        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            raise ValueError("SECRET_KEY environment variable is missing or empty!")

        return cls(
            app_env=app_env,
            api_timeout=api_timeout,
            secret_key=secret_key,
        )


if __name__ == "__main__":
    config = Settings.load()
    print("Configuration loaded successfully!")
    print(f"Environment: {config.app_env}")
    print(f"Timeout: {config.api_timeout}s")
    print(f"Secret key masked: {config.secret_key[:3]}***")
