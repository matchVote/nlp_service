import pytest

from nlp import Classifier


class TestClassifier:

    def test_classification_returns_political_if_text_contains_official_names(self):
        text = 'Hey there, Sherrod brown!'
        assert Classifier(text).classification == 'political'

    def test_is_political_returns_none_if_text_does_not_contain_official_names(self):
        text = 'No politics here.'
        assert not Classifier(text).classification
