from os import name
from sqlalchemy import insert, select, text, update
from database import sync_engine, async_engine, Base
from models import workers_table


class SyncCore:

    @staticmethod
    def create_tables() -> None:
        # sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        # sync_engine.echo = True

    @staticmethod
    def insert_workers() -> None:
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

    @staticmethod
    def select_workers() -> None:
        with sync_engine.connect() as conn:
            query = select(workers_table)
            result = conn.execute(query)
            workers = result.all()
            print(workers)

    @staticmethod
    def update_worker(worker_name: str, worker_id: int) -> None:
        with sync_engine.connect() as conn:
            # stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            # stmt = stmt.bindparams(username=worker_name, id=worker_id)
            stmt = (
                update(workers_table)
                .values(username=worker_name)
                # .where(workers_table.c.id == worker_id)
                .filter_by(id=worker_id)
                
            )
            conn.execute(stmt)
            conn.commit()


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
