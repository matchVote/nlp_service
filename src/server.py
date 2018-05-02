import os

from sanic import Sanic
from sanic.response import json, text

from src import nlp

app = Sanic()


@app.route('/parse_publisher', methods=['POST'])
async def parse_publisher(request):
    url = request.json.get('url')
    article_urls = nlp.parse_publisher(url)
    return json({'article_urls': article_urls})


@app.route('/parse_article', methods=['POST'])
async def extract(request):
    html = request.json.get('html')
    data = nlp.parse_article(html)
    return json(data)


@app.route('/classify', methods=['POST'])
async def classify(request):
    text = request.json.get('text')
    return json({'classification': nlp.classify(text)})


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    text = request.json.get('text')
    title = request.json.get('title')
    summary, keywords = nlp.extract_summary_and_keywords(text, title)
    data = {
        'read_time': nlp.calculate_read_time(text),
        'mentioned_officials': nlp.mentioned_officials(text),
        'summary': summary,
        'keywords': keywords,
        }
    return json(data)


@app.route('/hc', methods=['GET'])
async def hc(request):
    return text('ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('SERVICE_PORT'), access_log=True)
