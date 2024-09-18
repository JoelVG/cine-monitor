from pydantic import BaseModel, Field, AliasChoices
from typing import Optional


class Movie(BaseModel):
    title: str
    duration: Optional[str] = Field(default="")
    actors: Optional[str] = Field(alias="Actor", default="")
    director: Optional[str] = Field(alias="Director", default="")
    category: Optional[str] = Field(validation_alias=AliasChoices("Género", "Genre"))
    date: Optional[str] = Field(
        validation_alias=AliasChoices("Estreno", "Release"), default=""
    )
    language: Optional[str] = Field(
        validation_alias=AliasChoices("Idioma", "Language"), default=""
    )
    in_cinema: bool = True


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
