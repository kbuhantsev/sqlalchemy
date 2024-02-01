from sqlalchemy import text
from database import sync_engine, async_engine
from models import metadata_obj


def get_version_sync():
    with sync_engine.connect() as conn:  # begin() будет делать коммит автоматом
        res = conn.execute(text("SELECT VERSION()"))
        # print(res.all()) # first() all() one()
        # [('PostgreSQL 16.1 (Debian 12.2.0-14) 12.2.0, 64-bit',)]
        # print(res.first())
        # ('PostgreSQL 16.1 (Debian 12.2.0-14) 12.2.0, 64-bit',)
        print(res.first())
        conn.commit()


async def get_version_async():
    async with async_engine.connect() as conn:  # begin() будет делать коммит автоматом
        res = await conn.execute(text("SELECT VERSION()"))
        print(res.first())


def create_tables():
    metadata_obj.create_all(sync_engine)
