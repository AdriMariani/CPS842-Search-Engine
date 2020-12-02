from flask import Flask, request, Response
from search import Search
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
search = Search('crawler/pages.json')

@app.route('/query', methods=['POST'])
def query():
    body = request.get_json()
    if "start" in body and "end" in body:
        start = body['start']
        end = body['end']
        resp = Response(json.dumps(search.query(body['query'])[start:end]))
    else:
        resp = Response(json.dumps(search.query(body['query'])))
    resp.headers["Content-Type"] = 'application/json'
    return resp