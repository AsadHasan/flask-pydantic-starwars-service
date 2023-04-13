from typing import Annotated

from pydantic import BaseModel, conlist

from src.model.result import Result


class People(BaseModel):
    count: int
    next: str | None
    previous: str | None
    results: Annotated[list[Result], conlist(str, unique_items=True)]

    class Config:
        frozen = True
