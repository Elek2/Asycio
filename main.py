import asyncio
import aiohttp
from time import time
import numpy

from models import Session, StarPeople, engine, Base


# получаем пользователей по одному
async def person_get(pers_id):
    session = aiohttp.ClientSession()
    response = await session.get(f"https://swapi.dev/api/people/{pers_id}")
    person_json = await response.json()

    # исключаем ненужные поля из запроса через вычитание кол-во полей в табл и в запросе
    table_columns = StarPeople.__table__.columns.keys()
    excluded_fields = set(person_json).difference(set(table_columns))
    for field in excluded_fields:
        person_json.pop(field)

    # проверяем поля содержащие списки ссылок
    for attribute in person_json:
        if isinstance(person_json.get(attribute), list):
            person_json[attribute] = await link_name_convert(person_json.get(attribute))

    await session.close()
    return person_json


# изменяем в списках ссылок ссылки на имена
async def link_name_convert(links: list) -> list:
    session = aiohttp.ClientSession()
    names_list = []
    for link in links:
        response = await session.get(link)
        response_json = await response.json()
        name = response_json.get('name')
        if not name:
            name = response_json.get('title')
        names_list.append(name)

    await session.close()
    return names_list


# заносим в базу данных
async def person_put_bd(person_json):
    async with Session() as s:
        new_person_list = [StarPeople(**i) for i in person_json]
        s.add_all(new_person_list)
        await s.commit()


async def main():
    async with engine.begin() as s:
        await s.run_sync(Base.metadata.drop_all)
        await s.run_sync(Base.metadata.create_all)

    for chunk in numpy.array_split(range(1, 83), 10):
        ten_person = [person_get(i) for i in chunk]
        person_json = await asyncio.gather(*ten_person)
        asyncio.create_task(person_put_bd(person_json))
        await person_put_bd(person_json)
        # asyncio.create_task(person_put_bd(person_json))
    # current_task = asyncio.current_task()
    # tasks = asyncio.all_tasks()
    # tasks.remove(current_task)
    # await asyncio.gather(*tasks)

    await engine.dispose()

if __name__ == '__main__':
    start = time()
    asyncio.run(main())
    print(time() - start)
