import requests
from models import StarPeople

from models import Session


def person_get(pers_id):
    response = requests.get(f"https://swapi.dev/api/people/{pers_id}")
    return response.json()


def link_name_convert(links: list) -> list:
    names_list = []
    for link in links:
        response = requests.get(link)
        name = response.json().get('name')
        if not name:
            name = response.json().get('title')
        names_list.append(name)
    return names_list


def put_into_db(pers_id):
    with Session() as s:
        table_columns = StarPeople.__table__.columns.keys()
        person = person_get(pers_id)
        excluded_fields = set(person).difference(set(table_columns))
        for field in excluded_fields:
            person.pop(field)

        for parameter in person:
            if isinstance(person.get(parameter), list):
                person[parameter] = link_name_convert(person.get(parameter))

        new_person = StarPeople(**person)
        s.add(new_person)
        s.commit()

        check_person = s.query(StarPeople).get(new_person.id)
        print(check_person.name)


if __name__ == '__main__':
    put_into_db(1)
