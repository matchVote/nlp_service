import pytest

from src import nlp


class TestNLP:

    def test_classify_returns_political_if_text_contains_official_names(self):
        text = 'Hey there, Sherrod brown!'
        assert nlp.classify(text) == 'political'

    def test_classify_returns_none_if_text_does_not_contain_official_names(self):
        text = 'No politics here.'
        assert not nlp.classify(text)
