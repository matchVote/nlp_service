from sanic import Sanic
from sanic.response import json

from src import nlp

app = Sanic()


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
        'mentioned_officials_ids': nlp.mentioned_officials_ids(text),
        'summary': summary,
        'keywords': keywords,
        }
    return json(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
