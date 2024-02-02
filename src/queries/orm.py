from sqlalchemy import select
from database import sync_engine, session_factory, Base
from models import WorkersOrm


class SyncOrm:

    @staticmethod
    def create_tables() -> None:
        # sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        # sync_engine.echo = True

    @staticmethod
    def insert_workers() -> None:
        worker_bobr = WorkersOrm(username="Bobr")
        worker_volk = WorkersOrm(username="Volk")
        with session_factory() as session:
            session.add_all([worker_bobr, worker_volk])
            session.flush()  # отправляет изменения
            session.commit()

    @staticmethod
    def select_workers() -> None:
        with session_factory() as session:
            query = select(WorkersOrm)
            result = session.execute(query)
            workers = result.scalars().all()
            print(workers)

    @staticmethod
    def update_worker(worker_name: str, worker_id: int) -> None:
        with session_factory() as session:
            worker_inst = session.get(WorkersOrm, worker_id)  # 1 объект
            worker_inst.username = worker_name
            # session.expire_all()
            # session.refresh()
            session.commit()
