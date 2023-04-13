from pydantic import BaseModel

from src.model.gender import Gender


class Person(BaseModel):
    name: str
    height: int
    mass: int | str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: Gender

    class Config:
        frozen = True
        use_enum_values = True
