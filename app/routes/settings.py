from fastapi import APIRouter
from pydantic import BaseModel
from app.config import settings

router = APIRouter(prefix="/api/settings", tags=["Settings"])

class TelegramConfig(BaseModel):
    bot_token: str
    chat_id: str

@router.post("/telegram")
def update_telegram(config: TelegramConfig):
    settings.TELEGRAM_BOT_TOKEN = config.bot_token
    settings.TELEGRAM_CHAT_ID = config.chat_id
    return {"message": "Updated successfully"}
