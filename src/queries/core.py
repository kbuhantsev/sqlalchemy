from sqlalchemy import insert, text
from database import sync_engine, async_engine
from models import metadata_obj, workers_table


def get_version_sync() -> None:
    with sync_engine.connect() as conn:  # begin() будет делать коммит автоматом
        res = conn.execute(text("SELECT VERSION()"))
        # print(res.all()) # first() all() one()
        # [('PostgreSQL 16.1 (Debian 12.2.0-14) 12.2.0, 64-bit',)]
        # print(res.first())
        # ('PostgreSQL 16.1 (Debian 12.2.0-14) 12.2.0, 64-bit',)
        print(res.first())
        conn.commit()


async def get_version_async() -> None:
    async with async_engine.connect() as conn:  # begin() будет делать коммит автоматом
        res = await conn.execute(text("SELECT VERSION()"))
        print(res.first())


def create_tables() -> None:
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True


def insert_data():
    with sync_engine.connect() as conn:
        # stmt = """INSERT INTO workers (username) VALUES
        # ('Bobr'),
        # ('Volk');"""
        stmt = insert(workers_table).values(
            [{"username": "Bobr"}, {"username": "Volk"}]
        )
        # conn.execute(text(stmt))
        conn.execute(stmt)
        conn.commit()
