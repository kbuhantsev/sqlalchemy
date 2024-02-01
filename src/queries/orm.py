from database import sync_engine, session_factory
from models import metadata_obj, WorkersOrm


def create_tables() -> None:
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True


def insert_data() -> None:
    worker_bobr = WorkersOrm(username="Bobr")
    worker_volk = WorkersOrm(username="Volk")
    with session_factory() as session:
        session.add_all([worker_bobr, worker_volk])
        session.commit()
