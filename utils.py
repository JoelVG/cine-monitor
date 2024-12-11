from pydantic import BaseModel
from typing import List
from constants import DEFAULT_HEADERS, BOT_URL
from models.movie import Movie
from requests import get as request_get
from http.client import RemoteDisconnected
from urllib3.exceptions import ReadTimeoutError
import aiohttp
from time import sleep
from bs4 import BeautifulSoup
from os import path as os_path
from urllib.parse import quote_plus
import csv
import time


def pydantic_to_csv(data: List[BaseModel], filename: str):
    """
    Function to convert list of Pydantic objects to CSV
    """
    if not data:
        print("The list is empty. No CSV file will be created.")
        return

    fieldnames = list(data[0].model_dump().keys())
    movies_title = [obj.title for obj in data]
    print("Movies: ", movies_title)
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for obj in data:
            writer.writerow(obj.model_dump())

    print(f"CSV file '{filename}' has been created successfully.")


def same_movies(movies: set[str], cine: str) -> bool:
    """
    Verify if the movies have been updated.
    """
    with open(cine, mode="r") as file:
        reader = csv.DictReader(file)
        existing_movies = set(row["title"] for row in reader)
        print("Existing movies: ", list(existing_movies))
        print("New movies: ", list(movies))
        return movies == existing_movies


def file_exists(path: str) -> bool:
    """
    Check if a file exists.
    """
    return os_path.isfile(path)


def get_movies_titles(url: str) -> List[str]:
    """
    Get movies titles from a given URL.
    """
    response = get_request(url, headers=DEFAULT_HEADERS)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    movies_ = soup.find(name="div", class_="list-content")
    return [
        title.text.strip()
        for title in movies_.find_all(name="h2", class_="entry-title")
    ]


def get_request(url: str, headers: dict[str, str] = DEFAULT_HEADERS):
    """
    Make a GET request to a given URL and return the HTML content.
    """
    try:
        # timeout = 120 because it is the max Skybox loading time
        response = request_get(url, headers=headers, timeout=120)
    except (ReadTimeoutError, RemoteDisconnected) as e:
        print(f"----------------ERROR: {e.__annotations__}----------------")
        sleep(5)
        response = request_get(url, headers=headers, timeout=5)
    if response.status_code == 200:
        return response
    else:
        raise Exception(f"ERROR {response.status_code} making GET request to: {url}")


def get_movies_from_csv(csv_file: str) -> List[Movie]:
    """
    Extract movies from csv.
    """
    if file_exists(csv_file):
        with open(csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            movies = [Movie(**row) for row in reader]
        return movies
    else:
        # raise FileNotFoundError(f"File {csv_file} does not exist.")
        print(f"File {csv_file} does not exist.")
        return []


def send_message(text: str, chat_id: str):
    txt = quote_plus(text)
    url = BOT_URL + "sendMessage?text={}&chat_id={}".format(txt, chat_id)
    get_url(url)

    # url = f"{BOT_URL}/sendMessage"
    # payload = {"text": text, "chat_id": chat_id}
    # response = request_get(url, params=payload)
    # return response.text


def get_url(url: str) -> str:
    response = request_get(url)
    content = response.content.decode("utf8")
    return content


def get_file_modified_date(file_path: str) -> float:
    """
    Get the modified date of a file.
    """
    creation_time = os_path.getmtime(file_path)
    return creation_time


def is_older_than_two_days(file_path: str) -> bool:
    """
    Check if a file is older than two days.
    """
    creation_time = get_file_modified_date(file_path)
    current_time = time.time()
    two_days_ago = current_time - (48 * 3600)  # 2 days in seconds H*S
    return creation_time < two_days_ago


async def async_get_request(url: str, headers: dict[str, str] = DEFAULT_HEADERS) -> str:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.text()
