
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import Column, String, DateTime, Boolean, func

import config

engine = create_engine(config.DATABASE_URL, max_overflow=100, pool_size=50)

def get_session() -> Session:
    return scoped_session(sessionmaker(bind=engine))()

class BaseTable(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Podcast(BaseTable):
    __tablename__ = 'Podcasts'
    name = Column(String, nullable=False)
    rss_link = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    chat_id = Column(String, nullable=False)
    
class Uploader(BaseTable):
    __tablename__ = 'Uploaders'
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    link_to_podcast = Column(String, nullable=False)
    pubDate = Column(DateTime, nullable=False)
    link_mp3 = Column(String, nullable=False)

    
BaseTable.metadata.create_all(engine)
session = get_session()
session.bind = engine

