import asyncio
import requests
import aiohttp

from models import Session, StarPeople


async def person_get(pers_id):
    session = aiohttp.ClientSession()
    response = await session.get(f"https://swapi.dev/api/people/{pers_id}")
    await session.close()
    return await response.json()


# async def link_name_convert(links: list) -> list:
#     names_list = []
#     for link in links:
#         response = requests.get(link)
#         name = response.json().get('name')
#         if not name:
#             name = response.json().get('title')
#         names_list.append(name)
#     return names_list


async def put_into_db(pers_id):
    with Session() as s:
        table_columns = StarPeople.__table__.columns.keys()
        person = await person_get(pers_id)
        excluded_fields = set(person).difference(set(table_columns))
        for field in excluded_fields:
            person.pop(field)

        # for parameter in person:
        #     if isinstance(person.get(parameter), list):
        #         person[parameter] = link_name_convert(person.get(parameter))

        new_person = StarPeople(**person)
        s.add(new_person)
        s.commit()

        check_person = s.query(StarPeople).get(new_person.id)
        print(check_person.name)


if __name__ == '__main__':
    asyncio.run(put_into_db(1))
    # put_into_db(1)
