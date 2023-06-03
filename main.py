import requests
import time
from models import StarPeople

from models import Session


def person_get(pers_id):
    response = requests.get(f"https://swapi.dev/api/people/{pers_id}")
    return response


# перебираем поля где есть списки ссылок и меняем ссылки на названия
def link_name_convert(links: list) -> list:
    names_list = []
    for link in links:
        response = requests.get(link)
        name = response.json().get('name')
        if not name:
            name = response.json().get('title')
        names_list.append(name)
    return names_list


def main():
    with Session() as s:
        # кол-во колонок из таблицы
        table_columns = StarPeople.__table__.columns.keys()

        # пока есть в базе - перебираем всех people
        status_code = 200
        pers_id = 1
        while status_code == 200:
            response = person_get(pers_id)
            person = response.json()
            status_code = response.status_code

            # исключаем из полученных данных ненужные поля
            excluded_fields = set(person).difference(set(table_columns))
            for field in excluded_fields:
                person.pop(field)

            # где в полях ссылки - заменяем на названия
            for parameter in person:
                if isinstance(person.get(parameter), list):
                    person[parameter] = link_name_convert(person.get(parameter))

            # добавляем в базу данных
            new_person = StarPeople(**person)
            s.add(new_person)
            s.commit()

            pers_id += 1
            print(person.get('name'))

            # заглушка - перебираем максимум 5 человек
            if pers_id > 5:
                status_code = 404


if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time()-start)
