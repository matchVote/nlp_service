import pytest

from src import nlp
from src.models import Official


class TestNLP:

    big_text = """
    My name is sherrod brown and my friend william clinton (not related to
    George clinton) knows that my name is sherrod BROWN. I also know
    barack obama and barack obama he knows my name, ShErrod brown.
    """

    @classmethod
    def setup_class(cls):
        """Populate DB"""
        Official.create(first_name='Sherrod',
                        last_name='Brown', mv_key='sherrod-brown')
        Official.create(first_name='William',
                        last_name='Clinton', mv_key='william-clinton')
        Official.create(first_name='Barack',
                        last_name='Obama', mv_key='barack-obama')
        Official.create(first_name='Bobeck',
                        last_name='Kuberdoodles',
                        birthday='1919-12-31',
                        mv_key='bobeck-kuberdoodles')
        Official.create(first_name='Arcus',
                        last_name='Post',
                        birthday='1920-01-01',
                        mv_key='arcus-post')

    @classmethod
    def teardown_class(cls):
        """Clear DB"""
        Official.delete().execute()

    def official_ids(self):
        sherrod = Official.select().where(Official.first_name == 'Sherrod')[0]
        bill = Official.select().where(
            Official.first_name == 'William',
            Official.last_name == 'Clinton')[0]
        obama = Official.select().where(Official.first_name == 'Barack')[0]
        return [str(sherrod.id), str(bill.id), str(obama.id)]

    def find_official(self, officials, id):
        for official in officials:
            if official['official_id'] == id:
                return official

    def test_classify_returns_political_if_text_contains_official_names(self):
        text = 'Hey there, Arcus Post!'
        assert nlp.classify(text) == 'political'

    def test_classify_returns_includes_officials_with_no_birthday_data(self):
        text = 'Hey there, Sherrod brown!'
        assert nlp.classify(text) == 'political'

    def test_classify_returns_none_if_text_does_not_contain_official_names(self):
        text = 'No politics here.'
        assert not nlp.classify(text)

    def test_classify_ignores_officials_born_before_birthday_cutoff(self):
        text = 'Hey there, Bobeck Kuberdoodles!'
        assert not nlp.classify(text)

    def test_mentioned_officials_provides_ids(self):
        results = nlp.mentioned_officials(self.big_text)
        ids = [official['official_id'] for official in results]
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

    def test_extract_first_full_name_returns_full_name_of_first_author(self):
        data = ['Hey Bo something again', 'anything', '...']
        assert nlp._extract_first_full_name(data) == ['Hey Bo']
        assert nlp._extract_first_full_name(['Bob Jones']) == ['Bob Jones']

    def test_extract_first_full_name_returns_empty_list_with_no_match(self):
        assert nlp._extract_first_full_name([]) == []
        assert nlp._extract_first_full_name(['what']) == []

    def test_force_https_converts_http_urls_into_https(self):
        assert nlp._force_https('http://hey.com') == 'https://hey.com'
        assert nlp._force_https('https://you.com') == 'https://you.com'
