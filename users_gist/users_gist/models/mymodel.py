from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode)
    last_name = Column(Unicode)
    user_name = Column(Unicode)
    email = Column(Unicode)
    fav_food = Column(Unicode)
    password = Column(Unicode)


Index('my_index', MyModel.id, unique=True, mysql_length=255)
