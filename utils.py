from pydantic import BaseModel
from typing import List
from constants import NOT_CATEGORIES, DEFAULT_HEADERS
from requests import get as request_get
from http.client import RemoteDisconnected
from urllib3.exceptions import ReadTimeoutError
from time import sleep
from bs4 import BeautifulSoup
from os import path as os_path
import csv


def extract_time(time: str) -> str:
    """
    Extract the time from a string from format:
    01 hours 46 minutes to "HH:MM".
    """
    text = time.split(" ")
    h = int(text[0])
    m = int(text[2])
    return f"{h:02d}:{m:02d}"


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


def clean_categories(text: str) -> str:
    """
    Remove banned words category.
    """
    return ", ".join(
        word.strip() for word in text.split(",") if word.strip() not in NOT_CATEGORIES
    )


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


def get_movies_titles(url: str) -> set[str]:
    """
    Get movies titles from a given URL.
    """
    response = get_request(url, headers=DEFAULT_HEADERS)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    movies_ = soup.find(name="div", class_="list-content")
    return set(
        title.text.strip()
        for title in movies_.find_all(name="h2", class_="entry-title")
    )


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
