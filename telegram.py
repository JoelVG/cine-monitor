import json
import requests
import urllib

from constants import BOT_URL


def get_url(url: str) -> str:
    response = requests.get(url)
    return response.content.decode("utf8")


def get_json_from_url(url: str):
    content = get_url(url)
    return json.loads(content)


def get_updates(offset=None):
    url = BOT_URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    return get_json_from_url(url)


def get_last_update_id(updates):
    update_ids = [int(update["update_id"]) for update in updates["result"]]
    return max(update_ids)


def echo_all(updates):
    from commands import run_command

    for update in updates["result"]:
        if update.get("message") is not None:
            if update.get("message", {}).get("text") is not None:
                text = update["message"]["text"].lower().strip()
                chat = update["message"]["chat"]
                print("Mensaje recibido: ", text)
                print("Chat info: ", chat)
                username = (
                    chat["username"]
                    if chat.get("username")
                    else chat["first_name"] + " " + chat["last_name"]
                )
                user = {"username": username, "chat_id": str(chat["id"])}
                run_command(text, user)


def send_message(text: str, chat_id: str):
    txt = urllib.parse.quote_plus(text)
    url = BOT_URL + "sendMessage?text={}&chat_id={}".format(txt, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates is not None:
            if len(updates.get("result", [])) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)
            # Maybe you forgot to export your BOT TOKEN to .env
            elif updates.get("ok") is False:
                break


if __name__ == "__main__":
    main()
