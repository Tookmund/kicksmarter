#!/usr/bin/env python3
from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(hello='World!')

@app.route('/api', methods=['POST'])
def api():
    # Data in request.form
    return jsonify({
        'chance': 50,
        'similar': [
                {
                    'title': 'hello world',
                    'url': 'https://example.com'
                }
            ]
    })

@app.after_request
def apply_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == "__main__":
    app.run()
