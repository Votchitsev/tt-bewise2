import uuid
import databases
import ormar
import sqlalchemy
from typing import Optional 

from .config import settings


database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'users'

    id: int = ormar.Integer(primary_key=True)
    uuid: str = ormar.UUID(uuid_format='string', default=uuid.uuid1)
    name: str = ormar.String(unique=True, max_length=50)


class Files(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'files'

    id: int = ormar.UUID(primary_key=True, uuid_format='string', default=uuid.uuid1)
    path: str = ormar.String(max_length=100)
    user: User = ormar.ForeignKey(User)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
