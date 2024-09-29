from pydantic import BaseModel
from typing import List
from constants import NOT_CATEGORIES
import csv
import glob


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

    fieldnames = list(data[0].model_dump.keys())
    movies_title = [obj.title for obj in data]
    if verify_updated_movies(movies_title, filename):
        with open(f"{filename}.csv", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for obj in data:
                writer.writerow(obj.model_dump)

        print(f"CSV file '{filename}.csv' has been created successfully.")
    else:
        print(f"Movies from '{filename}' are already up to date.")


def clean_categories(text: str) -> str:
    """
    Remove banned words category.
    """
    return ", ".join(
        word.strip() for word in text.split(",") if word.strip() not in NOT_CATEGORIES
    )


def verify_updated_movies(movies: List[str], cine: str) -> bool:
    """
    Verify if the movies have been updated.
    """
    files = glob.glob(f"{cine}*.csv")
    if not files:
        print("File not found.")
        return False
    with open(files[0], mode="r") as file:
        reader = csv.DictReader(file)
        existing_movies = set(row["title"] for row in reader)
        return set(movies) == existing_movies
