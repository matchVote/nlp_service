from sanic import Sanic
from sanic.response import json

from nlp import Classifier

app = Sanic()


@app.route('/classify', methods=['POST'])
async def classify(request):
    text = request.json.get('text')
    return json({'classification': Classifier(text).classification})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
