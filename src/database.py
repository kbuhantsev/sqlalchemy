from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import MetaData, String, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings

metadata_obj = MetaData()

sync_engine = create_engine(
    url=settings.database_url_psycopg, echo=True, pool_size=5, max_overflow=10
)

# ASYNC
async_engine = create_async_engine(
    url=settings.database_url_asyncpg, echo=True, pool_size=5, max_overflow=10
)

session_factory = sessionmaker(sync_engine)
async_session_factory = sessionmaker(async_engine)

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self) -> str:
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
