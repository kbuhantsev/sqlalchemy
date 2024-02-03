from sqlalchemy import Integer, and_, func, select
from database import sync_engine, session_factory, Base
from models import ResumesOrm, WorkLoad, WorkersOrm


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


    @staticmethod
    def insert_resumes() -> None:
        with session_factory() as session:
            resume_jack_1 = ResumesOrm(
                title="Python Junior Developer", compensation=50000, workload=WorkLoad.fulltime, worker_id=1)
            resume_jack_2 = ResumesOrm(
                title="Python Разработчик", compensation=150000, workload=WorkLoad.fulltime, worker_id=1)
            resume_michael_1 = ResumesOrm(
                title="Python Data Engineer", compensation=250000, workload=WorkLoad.parttime, worker_id=2)
            resume_michael_2 = ResumesOrm(
                title="Data Scientist", compensation=300000, workload=WorkLoad.fulltime, worker_id=2)
            session.add_all([resume_jack_1, resume_jack_2, 
                             resume_michael_1, resume_michael_2])
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        having avg(compensation) > 70000
        """
        with session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    # 1 вариант использования cast
                    # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
                    # 2 вариант использования cast (предпочтительный способ)
                    func.avg(ResumesOrm.compensation).cast(Integer).label("avg_compensation"),
                )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(func.avg(ResumesOrm.compensation) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result[0].avg_compensation)