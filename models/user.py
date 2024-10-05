from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    username: str
    chat_id: str
    is_active: bool = True
    created_at: str = str(datetime.now())
    updated_at: str = ""
