import json
import requests
import urllib

from constants import BOT_URL


def get_url(url: str) -> str:
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url: str):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = BOT_URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = [int(update["update_id"]) for update in updates["result"]]
    return max(update_ids)


def echo_all(updates):
    from commands import run_command

    for update in updates["result"]:
        if update.get("message") is not None:
            if update.get("message", {}).get("text") is not None:
                text = update["message"]["text"].lower().strip()
                print("Mensaje recibido: ", text)
                user = {
                    "username": update["message"]["chat"]["username"],
                    "chat_id": str(update["message"]["chat"]["id"])
                }
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
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)


if __name__ == "__main__":
    main()