import json
import pytest

from src.models import Official
from src.server import app

with open('tests/support/sample_text.txt') as f:
    SAMPLE_TEXT = f.read()


class TestIntegration:

    def test_extract_returns_relevant_data(self):
        with open('tests/support/sample_article.html') as f:
            html = f.read()
        data = json.dumps({'html': html})
        _, response = app.test_client.post('/extract', data=data)

        expected_title = 'Net Neutrality Supporters Launch New Campaign To '\
            'Reverse Unpopular FCC Decision'
        assert response.status == 200
        assert response.json.get('title') == expected_title
        assert 'Ryan Grenoble' in response.json.get('authors')
        assert response.json.get('date_published')
        assert response.json.get('text')
        assert response.json.get('top_image_url')

    def test_classify_returns_unknown_when_text_does_not_match(self):
        data = json.dumps({'text': 'hey there'})
        _, response = app.test_client.post('/classify', data=data)
        assert response.status == 200
        assert response.json.get('classification') is None

    def test_classify_returns_political_when_text_contains_name_of_official(self):
        data = json.dumps({'text': 'When Reid Ribble started...'})
        _, response = app.test_client.post('/classify', data=data)
        assert response.status == 200
        assert response.json.get('classification') == 'political'

    def test_analyze_calculates_text_read_time_in_minutes_rounded_up(self):
        data = json.dumps({'text': SAMPLE_TEXT})
        _, response = app.test_client.post('/analyze', data=data)
        assert response.status == 200
        assert response.json.get('read_time') == 2

    def test_analyze_extracts_keywords(self):
        data = json.dumps({'text': SAMPLE_TEXT, 'title': 'Murakami lives'})
        _, response = app.test_client.post('/analyze', data=data)
        assert response.status == 200
        assert response.json.get('keywords')

    def test_analyze_extracts_summary(self):
        data = json.dumps({'text': SAMPLE_TEXT, 'title': 'Murakami lives'})
        _, response = app.test_client.post('/analyze', data=data)
        assert response.status == 200
        assert response.json.get('summary')

    def test_analyze_lists_all_known_officials_mentioned_in_text(self):
        text = """
        Once a trump man went to see heidi heitkamp and you what? Grace Meng
        showed up. Whoa Al!
        """
        data = json.dumps({'text': text, 'title': 'Murakami lives'})
        _, response = app.test_client.post('/analyze', data=data)
        expected_ids = compile_official_ids(['heitkamp', 'meng'])
        assert response.status == 200
        ids = sorted(response.json.get('mentioned_officials_ids'))
        print(f'expected ids: {expected_ids}')
        print(f'actual ids: {ids}')
        assert ids == expected_ids


def compile_official_ids(last_names):
    officials = Official.select().where(Official.last_name << last_names)
    return sorted(str(official.id) for official in officials)
