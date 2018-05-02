import pytest

from src import nlp
from src.models import Official


class TestNLP:

    big_text = """
    My name is sherrod brown and my friend william clinton (not related to
    George clinton) knows that my name is sherrod BROWN. I also know
    barack obama and barack obama he knows my name, ShErrod brown.
    """

    def official_ids(self):
        sherrod = Official.select().where(Official.first_name == 'sherrod')[0]
        bill = Official.select().where(
            Official.first_name == 'william',
            Official.last_name == 'clinton')[0]
        obama = Official.select().where(Official.first_name == 'barack')[0]
        return [str(sherrod.id), str(bill.id), str(obama.id)]

    def find_official(self, officials, id):
        for official in officials:
            if official['representative_id'] == id:
                return official

    def test_classify_returns_political_if_text_contains_official_names(self):
        text = 'Hey there, Sherrod brown!'
        assert nlp.classify(text) == 'political'

    def test_classify_returns_none_if_text_does_not_contain_official_names(self):
        text = 'No politics here.'
        assert not nlp.classify(text)

    def test_mentioned_officials_provides_ids(self):
        results = nlp.mentioned_officials(self.big_text)
        ids = [official['representative_id'] for official in results]
        expected_ids = self.official_ids()
        assert expected_ids == ids

    def test_mentioned_officials_provides_mentioned_counts(self):
        results = nlp.mentioned_officials(self.big_text)
        ids = self.official_ids()
        sherrod = self.find_official(results, ids[0])
        assert sherrod['mentioned_count'] == 3
        bill = self.find_official(results, ids[1])
        assert bill['mentioned_count'] == 1
        barack = self.find_official(results, ids[2])
        assert barack['mentioned_count'] == 2
