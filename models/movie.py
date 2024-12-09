from pydantic import BaseModel, Field, AliasChoices, validator
from typing import Optional

from constants import NOT_CATEGORIES


def extract_time(time: str) -> str:
    """
    Extract the time from a string from format:
    01 hours 46 minutes to "HH:MM".
    """
    text = time.split(" ")
    if len(text) == 1:  # It already comes with the HH:MM format
        return time
    h = int(text[0])
    m = int(text[2])
    return f"{h:02d}:{m:02d}"


def clean_categories(text: str) -> str:
    """
    Remove banned words category.
    """
    return ", ".join(
        word.strip() for word in text.split(",") if word.strip() not in NOT_CATEGORIES
    ).strip()


class Movie(BaseModel):
    title: str
    duration: Optional[str] = Field(default="")
    actors: Optional[str] = Field(
        validation_alias=AliasChoices("Actor", "actors"), default=""
    )
    director: Optional[str] = Field(
        validation_alias=AliasChoices("Director", "director"), default=""
    )
    category: Optional[str] = Field(
        validation_alias=AliasChoices("Género", "Genre", "category"), default=""
    )
    date: Optional[str] = Field(
        validation_alias=AliasChoices("Estreno", "Release", "date"), default=""
    )
    language: Optional[str] = Field(
        validation_alias=AliasChoices("Idioma", "Language", "language"), default=""
    )
    in_cinema: bool = True

    @validator("duration")
    def format_duration(cls, duration: str) -> str:
        if duration:
            return extract_time(duration)
        return duration

    @validator("category")
    def format_category(cls, category: str) -> str:
        if category:
            return clean_categories(category.lower())
        return category

    def __str__(self) -> str:
        message = f"🎬 *{self.title}*\n"

        if self.duration:
            message += f"🕒 Duration: {self.duration}:00\n"
        if self.date:
            message += f"📅 Release Date: {self.date}\n"
        if self.director:
            message += f"🎬 Director: {self.director}\n"
        if self.actors:
            message += f"🎭 Actors: {self.actors}\n"
        if self.category:
            message += f"🏷️ Category: {self.category}\n"
        if self.language:
            message += f"🗣️ Language: {self.language}\n"
        message += f"🎟️ {'In Cinema' if self.in_cinema else 'Coming Soon'}\n"

        return message.strip()
