from requests import Response, request

from src.model.people import People
from src.model.person import Person
from src.model.result import Result


def _get_person_from_result(result: Result) -> Person:
    person = result.dict(
        exclude={
            "homeworld",
            "films",
            "species",
            "vehicles",
            "starships",
            "created",
            "edited",
            "url",
        }
    )
    return Person(**person)


def get_response(url: str) -> Response:
    response: Response = request(method="GET", url=url, timeout=90)
    response.raise_for_status()
    return response


def get_all_people(people: People) -> list[Result]:
    next_page: str | None = people.next
    results: list[Result] = people.results
    while next_page:
        next_people: People = People(**get_response(next_page).json())
        results.extend(next_people.results)
        next_page = next_people.next
    return results


def get_tallest_person(people: list[Result]) -> Person:
    tallest_person: Result = max(
        (person for person in people if person.height != "unknown"),
        key=lambda person: person.height,
    )
    return _get_person_from_result(tallest_person)


def get_shortest_person(people: list[Result]) -> Person:
    shortest_person: Result = min(
        (person for person in people if person.height != "unknown"),
        key=lambda person: person.height,
    )
    return _get_person_from_result(shortest_person)


def get_people_by_height_descending_order(people: list[Result]) -> list[Person]:
    return sorted(
        (
            _get_person_from_result(result)
            for result in people
            if isinstance(result.height, int)
        ),
        key=lambda result: result.height,
        reverse=True,
    )
