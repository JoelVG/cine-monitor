from typing import List
from constants import COMMANDS, TEST_MESSAGE, PRIM_OUTPUT, SKYBOX_OUTPUT
from skybox import get_skybox_movies
from prime import get_prime_movies
from utils import get_movies_from_csv, send_message
from models.movie import Movie
from user import UserCRUD, User


user_db = UserCRUD()


def get_movies() -> tuple[List[Movie], List[Movie]]:
    get_skybox_movies()
    get_prime_movies()
    prime_movies = get_movies_from_csv(PRIM_OUTPUT)
    skybox_movies = get_movies_from_csv(SKYBOX_OUTPUT)
    if prime_movies and skybox_movies:
        print("Movies loaded successfully")
        return prime_movies, skybox_movies
    else:
        return None


def run_command(command: str, user_: dict) -> None:
    if command in COMMANDS:
        user = User(**user_)
        print(user)

        if command == "test":
            print(send_message(TEST_MESSAGE, user.chat_id))
        elif command == "add":
            if user_db.read_user(user.chat_id) is None:
                user_db.create_user(user)
                send_message(f"Hola {user.username} 👤", user.chat_id)
                prime_movies, skybox_movies = get_movies()
                send_message("Peliculas de Prime: ", user.chat_id)
                for movie in prime_movies:
                    send_message(str(movie), user.chat_id)
                send_message("Peliculas de Skybox: ", user.chat_id)
                for movie in skybox_movies:
                    send_message(str(movie), user.chat_id)
            else:
                send_message("Ya estas registrado! 👀", user.chat_id)
        elif command == "remove":
            if user_db.read_user(user.chat_id) is not None:
                user_db.modify_user(user.chat_id, is_active=False)
                send_message("Adiós vaquero! 🎻", user.chat_id)
            else:
                send_message("No estas registrado! 👀", user.chat_id)
        elif command == "set":
            send_message("Comando en construcción...", user.chat_id)
            ...
    else:
        print("COMANDO NO VALIDO: ", command)
        send_message("Comando no disponible 😿", user_["chat_id"])
        send_message(f"Los comandos disponibles son: {COMMANDS}", user_["chat_id"])
