from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, conlist

from src.model.gender import Gender


class Result(BaseModel):
    name: str
    height: int | str
    mass: int | str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: Gender
    homeworld: str
    films: Annotated[list[str], conlist(str, unique_items=True)]
    species: Annotated[list[str], conlist(str, unique_items=True)]
    vehicles: Annotated[list[str], conlist(str, unique_items=True)]
    starships: Annotated[list[str], conlist(str, unique_items=True)]
    created: datetime
    edited: datetime
    url: str

    class Config:
        frozen = True
        use_enum_values = True
