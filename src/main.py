import os
from configparser import ConfigParser
from typing import Any

from flask import Flask
from requests import Response

from src.model.people import People
from src.model.person import Person
from src.model.result import Result
from src.service.starwars import (get_all_people,
                                  get_people_by_height_descending_order,
                                  get_response, get_shortest_person,
                                  get_tallest_person)

app: Flask = Flask(__name__)
config: ConfigParser = ConfigParser()
config.read("app.conf")
base_url: str = os.environ.get("BASE_URL") or config["URLS"]["DEFAULT_BASE_URL"]


def _get_all_ppl() -> list[Result]:
    resp: Response = get_response(f"{base_url}/people")
    ppl: People = People(**resp.json())
    return get_all_people(ppl)


@app.route("/tallest")
def get_tallest() -> str:
    return get_tallest_person(_get_all_ppl()).json()


@app.route("/shortest")
def get_shortest() -> str:
    return get_shortest_person(_get_all_ppl()).json()


@app.route("/all")
def get_all() -> list[dict[str, Any]]:
    people: list[Person] = get_people_by_height_descending_order(_get_all_ppl())
    return [person.dict() for person in people]
