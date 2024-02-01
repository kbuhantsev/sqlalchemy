# from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy import MetaData
from database import Base
from sqlalchemy.orm import mapped_column, Mapped


# Декларативный подход
class WorkersOrm(Base):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]


metadata_obj = MetaData()

# Императивный подход
# workers_table = Table(
#     "workers",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("username", String),
# )
