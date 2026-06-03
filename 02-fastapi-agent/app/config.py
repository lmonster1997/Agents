# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    dashscope_api_key: str
    llm_model: str = "qwen-turbo"
    max_tool_calls: int = 5
    log_level: str = "INFO"

    def model_post_init(self, __context):
        if not self.dashscope_api_key:
            raise ValueError("DASHSCOPE_API_KEY is required")

settings = Settings()