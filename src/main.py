from typing import Any

from flask import Flask
from flask import Response as Resp
from flask import jsonify, request
from requests import Response

from src.model.character import Character
from src.model.people import People
from src.model.person import Person
from src.model.result import Result
from src.service.starwars import (get_all_people,
                                  get_people_by_height_descending_order,
                                  get_response, get_shortest_person,
                                  get_tallest_person)

from . import base_url, create_app, db

app: Flask = create_app()


def _get_all_ppl() -> list[Result]:
    resp: Response = get_response(f"{base_url}/people")
    ppl: People = People(**resp.json())
    return get_all_people(ppl)


@app.route("/tallest", methods=["GET"])
def get_tallest() -> dict[str, Any]:
    return get_tallest_person(_get_all_ppl()).dict()


@app.route("/shortest", methods=["GET"])
def get_shortest() -> dict[str, Any]:
    return get_shortest_person(_get_all_ppl()).dict()


@app.route("/all", methods=["GET"])
def get_all():
    people: list[Person] = get_people_by_height_descending_order(_get_all_ppl())
    return [person.dict() for person in people]


@app.route("/custom-tallest-character", methods=["POST"])
def create_character() -> dict[str, Any]:
    tallest_person: dict[str, Any] = get_tallest_person(_get_all_ppl()).dict()
    tallest_person["nickname"] = request.get_json()["nickname"]

    character: Character = Character(**tallest_person)
    db.session.add(character)
    db.session.commit()
    return tallest_person


@app.route("/custom-tallest-character/<nickname>", methods=["GET"])
def get_character(nickname: str) -> dict[str, Any]:
    return jsonify(
        Character.query.filter_by(nickname=request.view_args["nickname"]).first()
    )


@app.route("/custom-tallest-character/<nickname>", methods=["DELETE"])
def delete_character(nickname: str) -> Resp:
    db.session.delete(
        Character.query.filter_by(nickname=request.view_args["nickname"]).first()
    )
    db.session.commit()
    return Resp(status=200)
