from flask import Flask, request

app = Flask(__name__)


@app.route("/<path:subpath>", methods=['GET', 'POST'])
def hello_world(subpath):
    method = request.method
    body = request.json
    headers = request.headers
    print(f"headers: {headers}\nbody: {body}\n")
    return {
        "code": 0,
        "data": {
            "id": 123,
            "name": "jack",
            "age": 32
        }
    }
