import json
import pytest

from nlp.server import app


class TestIntegration:

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
