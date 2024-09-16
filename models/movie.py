from pydantic import BaseModel, Field
from typing import Optional


class Movie(BaseModel):
    title: str
    duration: str
    actors: Optional[str] = Field(alias="Actor", default="")
    director: Optional[str] = Field(alias="Director")
    category: Optional[str] = Field(alias="Género")
    date: Optional[str] = Field(alias="Estreno")
    language: Optional[str] = Field(alias="Idioma")
    in_cinema: bool = True


# Actor:Eric Tsang
# Director:Yu Wang, Shixing Xu
# Género:Drama, En cartelera, Estrenos
# Estreno:12 septiembre, 2024
# Idioma:DOBLADO AL ESPAÑO
