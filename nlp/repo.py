import logging

import peewee

log = logging.getLogger(__name__)


class Repo:
    """Wrapper around model and database operations."""

    def __init__(self, model):
        self.model = model
        self.db = self.model._meta.database
        self.query = None

    def __getitem__(self, item):
        return self.query[item]

    def __iter__(self):
        for element in self.query:
            yield element

    def __len__(self):
        return len(self.query)

    def select(self, *fields):
        model_fields = [getattr(self.model, field) for field in fields]
        self.query = self.model.select(*model_fields)
        return self

    def where(self, **filters):
        clauses = self._convert_filters_to_clauses(filters)
        self.query = self.query.where(*clauses)
        return self

    def insert(self, entities):
        records = [dict(entity) for entity in entities]
        try:
            with self.db.atomic():
                self.model.insert_many(records).execute()
        except peewee.IntegrityError as error:
            log.warning(f'DB Insert IntegrityError: {error}')

    def _convert_filters_to_clauses(self, filters):
        return [getattr(self.model, field) == value
                for field, value in filters.items()]
