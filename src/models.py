import datetime
from sqlalchemy import ForeignKey, text
from database import Base, str_256
from sqlalchemy.orm import mapped_column, Mapped
from typing import Annotated
import enum

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        default=text("TIMEZONE('utc', now());"), onupdate=datetime.datetime.utcnow
    ),
]


class WorkLoad(enum.Enum):
    parttime = "parttime"
    worktime = "worktime"


# Декларативный подход
class WorkersOrm(Base):
    __tablename__ = "workers"
    id: Mapped[intpk]
    username: Mapped[str]


class ResumesOrm(Base):
    __tablename__ = "resumes"
    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int | None]
    workload: Mapped[WorkLoad]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# Императивный подход
# workers_table = Table(
#     "workers",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("username", String),
# )
