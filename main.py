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
    yourtitle = ''
    if request.is_json:
        try:
            yourtitle = request.get_json()['title']
        except Exception as e:
            return jsonify(exception=e)
    return jsonify({
        'chance': 50,
        'similar': [
                {
                    'title': yourtitle,
                    'url': 'https://example.com/your-request',
                    'category': 'category1',
                    'subcategory': 'subcat1',
                    'goal': 1,
                    'raised': 1,
                },
                {
                    'title': 'title2',
                    'url': 'https://example.com/url2',
                    'category': 'category2',
                    'subcategory': 'subcat2',
                    'goal': 2,
                    'raised': 2
                },
                {
                    'title': 'title3',
                    'url': 'https://example.com/url3',
                    'category': 'category3',
                    'subcategory': 'subcat3',
                    'goal': 3,
                    'raised': 3
                },
            ]
    })

if __name__ == "__main__":
    app.run()
