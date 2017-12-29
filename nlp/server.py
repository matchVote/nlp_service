from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route('/')
async def test(request):
    print(request)
    return json({'hello': 'there'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
