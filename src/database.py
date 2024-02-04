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
