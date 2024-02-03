from os import name
from sqlalchemy import insert, select, text, update, func, Integer, and_
from database import sync_engine, async_engine, Base
from models import WorkLoad, workers_table, resumes_table


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
                update(workers_table).values(username=worker_name)
                # .where(workers_table.c.id == worker_id)
                .filter_by(id=worker_id)
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def insert_resumes() -> None:
        with sync_engine.connect() as conn:
            resumes = [
                {
                    "title": "Python Junior Developer",
                    "compensation": 50000,
                    "workload": WorkLoad.fulltime,
                    "worker_id": 1,
                },
                {
                    "title": "Python Разработчик",
                    "compensation": 150000,
                    "workload": WorkLoad.fulltime,
                    "worker_id": 1,
                },
                {
                    "title": "Python Data Engineer",
                    "compensation": 250000,
                    "workload": WorkLoad.parttime,
                    "worker_id": 2,
                },
                {
                    "title": "Data Scientist",
                    "compensation": 300000,
                    "workload": WorkLoad.fulltime,
                    "worker_id": 2,
                },
            ]
            stmt = insert(resumes_table).values(resumes)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        having avg(compensation) > 70000
        """
        with sync_engine.connect() as conn:
            query = (
                select(
                    resumes_table.c.workload,
                    # 1 вариант использования cast
                    # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
                    # 2 вариант использования cast (предпочтительный способ)
                    func.avg(resumes_table.c.compensation)
                    .cast(Integer)
                    .label("avg_compensation"),
                )
                .select_from(resumes_table)
                .filter(
                    and_(
                        resumes_table.c.title.contains(like_language),
                        resumes_table.c.compensation > 40000,
                    )
                )
                .group_by(resumes_table.c.workload)
                .having(func.avg(resumes_table.c.compensation) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = conn.execute(query)
            result = res.all()
            print(result[0].avg_compensation)


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
