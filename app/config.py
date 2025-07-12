from pydantic_settings import BaseSettings

# Загрузка переменных окружения
class Settings(BaseSettings):
    DATABASE_URL: str
    API_LAYER_TOKEN: str
    SENTIMENT_API_URL: str
    HF_TOKEN: str
    NGROK_TOKEN: str
    NGROK_URL: str

    class Config:
        env_file = "app/.env"

settings = Settings()