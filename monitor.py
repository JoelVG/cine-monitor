#!/usr/bin/python
# Script to monitor new movies and send it to subscribers
import asyncio

from prime import get_prime_movies
from skybox import get_skybox_movies
from utils import get_movies_from_csv, send_message
from user import UserCRUD
from constants import SKYBOX_OUTPUT, PRIM_OUTPUT

user_db = UserCRUD()


async def get_movies():
    await asyncio.gather(get_prime_movies(), get_skybox_movies())


async def main():
    # Getting movies
    await get_movies()
    prime_movies = get_movies_from_csv(PRIM_OUTPUT)
    skybox_movies = get_movies_from_csv(SKYBOX_OUTPUT)

    # Getting users
    users = user_db.get_active_users()
    if not users:
        print("No active users")
        return
    else:
        # Sending movies to subscribers
        for user_ in users:
            send_message("PRIME MOVIES", user_.chat_id)
            for pmovie in prime_movies:
                send_message(str(pmovie), user_.chat_id)
            send_message("SKYBOX MOVIES", user_.chat_id)
            for smovie in skybox_movies:
                send_message(str(smovie), user_.chat_id)


if __name__ == "__main__":
    asyncio.run(main())
