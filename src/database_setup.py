import csv
import os
import time

from peewee import OperationalError

from src.database import Database
from src.models import Article, ArticleOfficial, Official

env = os.getenv('NLP_ENV')
db = Database()

if env in ['dev', 'test']:
    print(f'Setting up {env.upper()} environment...')
    # Check if DB exists and create it if it doesn't
    try:
        db.connect()
    except OperationalError:
        print('No DB found. Creating...')
        time.sleep(5)  # wait for postgres to be running in container
        db.create_database()
        db.create_hstore_extension()

    # Create tables
    db.create_tables([Article, Official, ArticleOfficial], safe=True)

    # Load officials
    print('Loading Official names... ', end='')
    Official.delete().execute()
    with open('config/rep_names.csv') as f:
        rows = csv.reader(f)
        next(rows)
        for first_name, last_name in rows:
            Official.create(
                first_name=first_name.lower(),
                last_name=last_name.lower())
    print(f'{len(Official.select())} total')
