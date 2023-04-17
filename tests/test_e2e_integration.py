import os
from configparser import ConfigParser
from typing import Any

from pytest import fixture
from requests import Response

from src.main import app
from src.model.people import People
from src.model.person import Person
from src.model.result import Result
from src.service.starwars import (
    get_all_people,
    get_people_by_height_descending_order,
    get_response,
    get_shortest_person,
    get_tallest_person,
)

config: ConfigParser = ConfigParser()
config.read("app.conf")
base_url: str = os.environ.get("BASE_URL") or config["URLS"]["DEFAULT_BASE_URL"]


@fixture
def get_people() -> tuple[list[Result], int]:
    resp: Response = get_response(f"{base_url}/people")
    ppl: People = People(**resp.json())
    return (get_all_people(ppl), ppl.count)


def test_e2e_integration(get_people: tuple[list[Result], int]) -> None:
    all_people, count = get_people
    assert len(all_people) == count
    tallest_person: Person = get_tallest_person(all_people)
    shortest_person: Person = get_shortest_person(all_people)
    assert isinstance(tallest_person.height, int)
    assert isinstance(shortest_person.height, int)
    assert tallest_person.height > shortest_person.height
    people_by_heights_in_descending_oder: list[
        Person
    ] = get_people_by_height_descending_order(all_people)
    assert all(
        isinstance(person.height, int)
        for person in people_by_heights_in_descending_oder
    )
    assert all(
        person.height <= people_by_heights_in_descending_oder[index - 1].height
        for index, person in enumerate(people_by_heights_in_descending_oder)
        if index > 1
    )


def test_api() -> None:
    response: Any = app.test_client().get("/all").get_json()
    assert response


@fixture
def nickname():
    return "Test123"


def test_custom_character_creation(nickname) -> None:
    response: Any = (
        app.test_client()
        .post("/custom-tallest-character", json={"nickname": nickname})
        .get_json()
    )
    assert response["nickname"] == nickname


def test_custom_character_retrieval(nickname) -> None:
    response: Any = (
        app.test_client().get(f"/custom-tallest-character/{nickname}").get_json()
    )
    assert response["nickname"] == nickname


def test_custom_character_deletion(nickname) -> None:
    response: Any = app.test_client().delete(f"/custom-tallest-character/{nickname}")
    assert response.status_code == 200
