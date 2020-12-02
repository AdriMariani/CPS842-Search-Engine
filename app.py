from flask import Flask, request, Response
from search import Search
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
search = Search('crawler/pages.json')

@app.route('/query', methods=['POST'])
def query():
    resp = Response(json.dumps(search.query(request.get_json()['query'])))
    resp.headers["Content-Type"] = 'application/json'
    return resp