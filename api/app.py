from fastapi import FastAPI

from models.telegram_webhook import TelegramWebhook
from commands import run_command

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Sup bot!"}


@app.post("/webhook")
async def webhook(webhook: TelegramWebhook):
    if webhook.message is not None:
        text = webhook.message.get("text").lower().strip()
        chat = webhook.message.get("chat")
        print("Mensaje recibido: ", text)
        username = (
            chat["username"]
            if chat.get("username")
            else chat["first_name"] + " " + chat["last_name"]
        )
        user = {"username": username, "chat_id": str(chat["id"])}
        await run_command(text, user)
    return {"ok": True}
