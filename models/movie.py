from pydantic import BaseModel, Field, AliasChoices
from typing import Optional


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

    def __str__(self) -> str:
        print("🎞️" * 40)
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


# Actor:Eric Tsang
# Director:Yu Wang, Shixing Xu
# Género:Drama, En cartelera, Estrenos
# Estreno:12 septiembre, 2024
# Idioma:DOBLADO AL ESPAÑO

# Actor:Brendan Gleeson, Catherine Keener, Harry Lawtey, Jacob Lofland
# Director:Todd Phillips
# Genre:Drama, Musical, Preventa, Próximamente, Suspenso
# Release:3 octubre, 2024
# Language:Doblada, Subtitulada
# Imdb:Mayores de 14 años
# Cinema:2D ATMOS – Subtitulada, 2D ATMOS – Doblada, 2D Normal
