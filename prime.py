import requests
from bs4 import BeautifulSoup
from models.movie import Movie
from typing import List
from constants import PRIME_NOW, PRIME_PREM
from utils import pydantic_to_csv, extract_time, clean_categories


def get_movies(url: str, in_cinema=True) -> List[Movie]:
    """
    Get movies from a given URL.
    """
    movies = []
    # We need this header to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")
    movies_ = soup.find_all(name="article", class_="entry-item clearfix")

    print(f"Found {len(movies_)} movies!")
    for movie in movies_:
        # Verify if we are at the end of the page
        title = movie.find(name="h2", class_="entry-title")
        if title:
            title = title.text.strip()
            print("Movie: ", title)
            movie_info = {
                info.label.text.replace(":", ""): info.span.text
                for info in movie.find(name="div", class_="entry-content").find(
                    name="ul",
                    class_="info-list"
                    # Special case cuz Cinema doesnt have span, also we dont need it
                )
                if info.label.text != "Cinema:"
            }
            movie_info["title"] = title
            # TODO add as validator model for duration field
            duration = movie.find(name="span", class_="duration")
            if duration:
                movie_info["duration"] = extract_time(duration.text.strip())
            movie_info["in_cinema"] = in_cinema
            m = Movie(**movie_info)
            if m.category:
                m.category = clean_categories(m.category.lower()).strip()
            movies.append(m)
        else:
            break
    return movies


in_cinema = get_movies(PRIME_NOW)
premieres = get_movies(PRIME_PREM, in_cinema=False)
in_cinema.extend(premieres)
pydantic_to_csv(in_cinema, "prime.csv")