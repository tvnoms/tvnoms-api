from pathlib import Path

import json
from typing import List

from pydantic.v1 import BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "TV Noms Backend"
    API_PATH: str = "/api/v1"
    JWT_SECRET: str = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

    BACKEND_CORS_ORIGINS: List[str] = [
        "https://frontend.example.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def parse_backend_cors_origins(cls, value):
        if value is None:
            return []

        if isinstance(value, str):
            normalized = value.strip()
            if not normalized:
                return []

            if normalized.startswith("["):
                try:
                    parsed = json.loads(normalized)
                except json.JSONDecodeError:
                    parsed = None
                if isinstance(parsed, list):
                    return parsed

            return [origin.strip() for origin in normalized.split(",") if origin.strip()]

        return value

    # Google OAuth settings
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    # GitHub OAuth settings
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    GITHUB_REDIRECT_URI: str = ""

    class Config:
        env_file = str(Path(__file__).resolve().parents[2] / ".env")
        case_sensitive = True

        @classmethod
        def parse_env_var(cls, field_name: str, raw_value: str):
            if field_name == "BACKEND_CORS_ORIGINS":
                normalized = raw_value.strip()
                if not normalized:
                    return []

                if normalized.startswith("["):
                    try:
                        parsed = json.loads(normalized)
                    except json.JSONDecodeError:
                        parsed = None
                    if isinstance(parsed, list):
                        return parsed

                return [origin.strip() for origin in normalized.split(",") if origin.strip()]

            return super().parse_env_var(field_name, raw_value)


settings = Settings()
