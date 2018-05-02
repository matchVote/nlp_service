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

    def test_classify_returns_political_if_text_contains_official_names(self):
        text = 'Hey there, Sherrod brown!'
        assert nlp.classify(text) == 'political'

    def test_classify_returns_none_if_text_does_not_contain_official_names(self):
        text = 'No politics here.'
        assert not nlp.classify(text)

    def test_mentioned_officials_returns_dict_with_ids_of_officials_as_keys(self):
        results = nlp.mentioned_officials(self.big_text)
        assert set(results.keys()) == set(self.official_ids())

    def test_mentioned_officials_returns_number_of_times_officials_are_mentioned(self):
        results = nlp.mentioned_officials(self.big_text)
        ids = self.official_ids()
        assert results[ids[0]] == 3
        assert results[ids[1]] == 1
        assert results[ids[2]] == 2
