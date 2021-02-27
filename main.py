#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction

app = Flask(__name__)

CORS(app)

app.config.from_pyfile('cockroach.cfg')

db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)

class UserIdea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    desc = db.Column(db.String)
    category = db.Column(db.String)
    amount = db.Integer

    def __init__(self, title, desc, category, amount):
        self.title = title
        self.desc = desc
        self.category = category
        self.amount = amount

#db.create_all()

@app.route('/')
def index():
    return jsonify(hello='World!')

@app.route('/api', methods=['HEAD', 'POST'])
def api():
    try:
        yourtitle = ''
        if request.is_json:
                yourtitle = request.get_json()['title']
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
    except Exception as e:
        return jsonify(exception=e), 400

@app.route('/db')
def dbroute():
    def callback(session):
        return jsonify(session.query(UserIdea).all())
    return run_transaction(sessionmaker, callback)

if __name__ == "__main__":
    app.run()
