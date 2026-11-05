from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "PricePulse AI"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./pricepulse.db"
    SECRET_KEY: str = "super-secret-key-change-in-production"
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    DISCORD_WEBHOOK_URL: str = ""
    DEFAULT_SCRAPING_INTERVAL_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
