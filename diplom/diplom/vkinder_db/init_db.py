from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def create_all(engine):
    Base.metadata.create_all(engine)


def drop_all(engine):
    Base.metadata.drop_all(engine)


class VKinderUsers(Base):
    __tablename__ = 'vkinder_user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String(1), nullable=False)
    city = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    vk_id = Column(String(250), nullable=False)


class VKinderSuggestions(Base):
    __tablename__ = 'vkinder_suggestion'

    partner_id = Column(Integer, primary_key=True)
    vk_id = Column(String(250), nullable=False)

    photos_1 = Column(String(250))
    photos_2 = Column(String(250))
    photos_3 = Column(String(250))
