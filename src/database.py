import os

from playhouse.postgres_ext import PostgresqlExtDatabase
import yaml


class Database:
    """Decorator for peewee database object."""

    def __init__(self):
        self.config = DatabaseConfig()
        self.db = setup_database(self.config)

    def __getattr__(self, attribute):
        return getattr(self.db, attribute)

    def create_database(self):
        command = 'createdb -h {host} -U {user} {database}'
        os.system(command.format(**self.config.mapping))

    def create_hstore_extension(self):
        cmd = "psql -h {host} -U {user} {database} -c 'CREATE EXTENSION hstore;'"
        os.system(cmd.format(**self.config.mapping))


class DatabaseConfig:
    """Wrapper around database configuration."""

    def __init__(self):
        self.env = os.getenv('NLP_ENV')
        self.mapping = self.load_config()

    def load_config(self):
        with open('config/database.yml') as f:
            config_string = f.read()
            if self.env == 'production':
                return {
                    'database': os.getenv('DB_NAME'),
                    'host': os.getenv('DB_HOST'),
                    'port': os.getenv('DB_PORT'),
                    'user': os.getenv('DB_USER'),
                    'password': os.getenv('DB_PASSWORD'),
                    }
            else:
                return yaml.load(config_string)[self.env]


def setup_database(config):
    return PostgresqlExtDatabase(**config.mapping)
