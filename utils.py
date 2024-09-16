from pydantic import BaseModel
from typing import List
from constants import NOT_CATEGORIES
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


def pydantic_to_csv(data: List[BaseModel], filename: str = "movies"):
    """
    Function to convert list of Pydantic objects to CSV
    """
    if not data:
        print("The list is empty. No CSV file will be created.")
        return

    fieldnames = list(data[0].dict().keys())

    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for obj in data:
            writer.writerow(obj.dict())

    print(f"CSV file '{filename}' has been created successfully.")


def clean_categories(text: str) -> str:
    """
    Remove banned words category.
    """
    return ", ".join(
        word for word in text.split(",") if word.strip() not in NOT_CATEGORIES
    )


# # Define a Pydantic model
# class Person(BaseModel):
#     name: str
#     age: int
#     city: str

# # Create a list of Person objects
# people = [
#     Person(name="Alice", age=30, city="New York"),
#     Person(name="Bob", age=25, city="Los Angeles"),
#     Person(name="Charlie", age=35, city="Chicago")
# ]

# # Convert the list of Person objects to CSV
# pydantic_to_csv(people, "people.csv")


# print(extract_time("01 hours 46 minutes"))
# print(clean_categories("Drama,  En cartelera,  Estrenos"))
