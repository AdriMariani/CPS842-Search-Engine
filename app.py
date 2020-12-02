from flask import Flask, request, Response
from search import Search
import json

app = Flask(__name__)
search = Search('crawler/pages.json')

@app.route('/query', methods=['POST'])
def query():
    resp = Response(json.dumps(search.query(request.get_json()['query'])))
    resp.headers["Content-Type"] = 'text/json'
    return resp