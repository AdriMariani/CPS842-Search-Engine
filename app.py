from flask import Flask, request
from search import Search

app = Flask(__name__)
search = Search('crawler/pages.json')

@app.route('/query', methods=['POST'])
def query():
    return search.query(request.get_json()['query'])
