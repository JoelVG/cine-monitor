import asyncio
from typing import List

from constants import COMMANDS, TEST_MESSAGE, PRIM_OUTPUT, SKYBOX_OUTPUT
from skybox import get_skybox_movies
from prime import get_prime_movies
from utils import get_movies_from_csv, send_message
from models.movie import Movie
from user import UserCRUD, User


user_db = UserCRUD()


async def get_movies() -> tuple[List[Movie], List[Movie]]:
    await asyncio.gather(get_prime_movies(), get_skybox_movies())
    prime_movies = get_movies_from_csv(PRIM_OUTPUT)
    skybox_movies = get_movies_from_csv(SKYBOX_OUTPUT)
    if prime_movies and skybox_movies:
        print("Movies loaded successfully")
        return prime_movies, skybox_movies
    else:
        raise Exception("Error loading movies")


async def run_command(command: str, user_: dict) -> None:
    """
    Run the command and send the message to the user.
    If you add a new command, you must add it to the COMMANDS list
    """
    if command in COMMANDS:
        user = User(**user_)

        if command == "test":
            print(send_message(TEST_MESSAGE, user.chat_id))
        elif command == "add":
            db_user = user_db.read_user(user.chat_id)
            if db_user is None:
                user_db.create_user(user)
                send_message(f"Hola {user.username} 👤", user.chat_id)

                prime_movies, skybox_movies = await get_movies()
                send_message("Peliculas de Prime: ", user.chat_id)
                for movie in prime_movies:
                    send_message(str(movie), user.chat_id)
                send_message("Peliculas de Skybox: ", user.chat_id)
                for movie in skybox_movies:
                    send_message(str(movie), user.chat_id)

            elif db_user.is_active:
                send_message("Ya estas registrado! 👀", user.chat_id)

            elif not db_user.is_active:
                user_db.modify_user(user.chat_id, is_active=True)
                send_message("Bienvenido de vuelta! 👻", user.chat_id)

                prime_movies, skybox_movies = await get_movies()
                send_message("Peliculas de Prime: ", user.chat_id)
                for movie in prime_movies:
                    send_message(str(movie), user.chat_id)
                send_message("Peliculas de Skybox: ", user.chat_id)
                for movie in skybox_movies:
                    send_message(str(movie), user.chat_id)
        elif command == "remove":
            db_user = user_db.read_user(user.chat_id)
            if db_user.is_active:
                user_db.modify_user(user.chat_id, is_active=False)
                send_message("Adiós vaquero! 🎻", user.chat_id)
            else:
                send_message("No estas registrado! 👀", user.chat_id)
        elif command == "prime":
            await get_prime_movies()
            prime_movies = get_movies_from_csv(PRIM_OUTPUT)
            if prime_movies:
                send_message("Peliculas de Prime: ", user.chat_id)
                for movie in prime_movies:
                    send_message(str(movie), user.chat_id)
            else:
                send_message("No hay peliculas de Prime", user.chat_id)
        elif command == "skybox":
            await get_skybox_movies()
            skybox_movies = get_movies_from_csv(SKYBOX_OUTPUT)
            if skybox_movies:
                send_message("Peliculas de Skybox: ", user.chat_id)
                for movie in skybox_movies:
                    send_message(str(movie), user.chat_id)
            else:
                send_message("No hay peliculas de Skybox", user.chat_id)
        elif command == "set":
            send_message("Comando en construcción...", user.chat_id)
            ...
    else:
        print("COMANDO NO VALIDO: ", command)
        send_message("Comando no disponible 😿", user_["chat_id"])
        send_message(f"Los comandos disponibles son: {COMMANDS}", user_["chat_id"])
