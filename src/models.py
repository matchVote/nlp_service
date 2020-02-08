from datetime import datetime
import uuid

from peewee import DateTimeField, IntegerField, Model, TextField, UUIDField
from playhouse.postgres_ext import ArrayField

from .database import Database


class BaseModel(Model):
    class Meta:
        database = Database()


class Article(BaseModel):
    """ORM model for articles table."""

    url = TextField(unique=True)
    title = TextField()
    authors = ArrayField(field_class=TextField, null=True)
    publisher = TextField()
    date_published = DateTimeField(null=True)
    keywords = ArrayField(field_class=TextField, null=True)
    summary = TextField(null=True)
    read_time = IntegerField(null=True)
    top_image_url = TextField(null=True)
    source = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'articles'


class Official(BaseModel):
    """ORM model for officials table."""

    id = UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = TextField()
    last_name = TextField()
    middle_name = TextField(null=True)
    official_name = TextField(null=True)
    mv_key = TextField()
    birthday = DateTimeField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'officials'


class ArticleOfficial(BaseModel):
    """Join table for articles and officials."""

    article_id = IntegerField()
    official_id = UUIDField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'articles_officials'
        indexes = (
            (('article_id', 'official_id'), True),
        )
