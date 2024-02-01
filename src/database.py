from typing import Any
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, CursorResult, create_engine, text

from config import settings


engine = create_engine(
    url=settings.database_url_psycopg, echo=True, pool_size=5, max_overflow=10
)

with engine.connect() as conn: # begin() будет делать коммит автоматом
    res: CursorResult[Any] = conn.execute(text("SELECT VERSION()"))
    # print(res.all()) # first() all() one()
    # [('PostgreSQL 16.1 (Debian 12.2.0-14) 12.2.0, 64-bit',)]
    #print(res.first())
    #('PostgreSQL 16.1 (Debian 12.2.0-14) 12.2.0, 64-bit',)
    print(res.first())
    conn.commit()
