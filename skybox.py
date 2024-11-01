from bs4 import BeautifulSoup
from typing import List
import asyncio
from models.movie import Movie
from constants import SKYBOX_NOW, SKYBOX_PREM, SKYBOX_OUTPUT
from utils import (
    pydantic_to_csv,
    extract_time,
    clean_categories,
    file_exists,
    same_movies,
    get_movies_titles,
    is_older_than_two_days,
    async_get_request,
)


async def get_movies(url: str, in_cinema=True) -> List[Movie]:
    """
    Get movies from a given URL.
    """
    movies = []
    html_content = await async_get_request(url)

    soup = BeautifulSoup(html_content, "html.parser")

    movies_ = soup.find(name="div", class_="list-content")
    print(f"Found {len(movies_)} movies!")
    for movie in movies_:
        skip_movie = False
        # Verify if we are at the end of the page
        title = movie.find(name="h2", class_="entry-title")
        if title:
            title = title.text.strip()
            print("Movie: ", title)
            movie_info = {
                info.label.text.replace(":", ""): info.span.text
                for info in movie.find(name="div", class_="entry-content").find(
                    name="ul", class_="info-list"
                )
            }
            movie_info["title"] = title
            # TODO add as validator model for duration field
            movie_info["duration"] = extract_time(
                movie.find(name="span", class_="duration").text.strip()
            )
            movie_info["in_cinema"] = in_cinema
            m = Movie(**movie_info)
            if m.category:
                # TODO improve >> avoid adding movies currently in cinema to premiers
                if "En cartelera" in m.category and not in_cinema:
                    skip_movie = True
                else:
                    # TODO add as validator model for category field
                    m.category = clean_categories(m.category.lower()).strip()
            if not skip_movie:
                movies.append(m)
        else:
            break
    return movies


async def get_all_movies() -> List[Movie]:
    """
    Get all movies from in cinema and premier.
    """
    in_cinema, premiers = await asyncio.gather(
        get_movies(SKYBOX_NOW), get_movies(SKYBOX_PREM, in_cinema=False)
    )
    return in_cinema + premiers


async def get_all_movies_titles() -> set[str]:
    """
    Get all movies titles from in cinema and premier.
    """
    in_cinema, premieres = await asyncio.gather(
        get_movies_titles(SKYBOX_NOW), get_movies_titles(SKYBOX_PREM)
    )
    return in_cinema | premieres


async def get_skybox_movies():
    # Verify if we already have the movies
    if file_exists(SKYBOX_OUTPUT) and not is_older_than_two_days(SKYBOX_OUTPUT):
        if await same_movies(await get_all_movies_titles(), SKYBOX_OUTPUT):
            print("No new movies for Skybox")
        else:
            movies = await get_all_movies()
            pydantic_to_csv(movies, SKYBOX_OUTPUT)
    else:
        # First time getting the movies
        movies = await get_all_movies()
        pydantic_to_csv(movies, SKYBOX_OUTPUT)


# if __name__ == "__main__":
#     asyncio.run(get_skybox_movies())
