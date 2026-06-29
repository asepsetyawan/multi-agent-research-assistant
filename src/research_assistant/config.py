from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    tavily_api_key: str | None = None
    max_research_iterations: int = 2
    max_subtasks: int = 4


@lru_cache
def get_settings() -> Settings:
    return Settings()
