
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field


# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


class Settings(BaseModel):
    """
    Stores all application configuration.
    """

    openrouter_api_key: str

    openrouter_model: str

    openrouter_base_url: str = (
        "https://openrouter.ai/api/v1"
    )

    database_path: Path = (
        BASE_DIR / "outputs" / "lesson_generator.db"
    )

    max_retries: int = Field(default=2, ge=0, le=2)


def get_settings() -> Settings:
    """
    Load application settings from environment variables.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is missing in .env file"
        )

    if not model:
        raise ValueError(
            "OPENROUTER_MODEL is missing in .env file"
        )

    return Settings(
        openrouter_api_key=api_key,
        openrouter_model=model,
        openrouter_base_url=os.getenv(
            "OPENROUTER_BASE_URL",
            "https://openrouter.ai/api/v1"
        ),
        database_path=Path(
            os.getenv(
                "DATABASE_PATH",
                str(BASE_DIR / "outputs" / "lesson_generator.db")
            )
        ),
        max_retries=2
    )


def validate_settings() -> bool:
    """
    Validate application configuration.
    """

    settings = get_settings()

    if not settings.openrouter_api_key.strip():
        raise ValueError("OpenRouter API key cannot be empty")

    if not settings.openrouter_model.strip():
        raise ValueError("OpenRouter model cannot be empty")

    return True
