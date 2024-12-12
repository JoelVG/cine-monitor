from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    created_at: str = str(datetime.now())
