#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return jsonify(hello='World!')

@app.route('/api', methods=['HEAD', 'POST'])
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

if __name__ == "__main__":
    app.run()
