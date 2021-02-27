#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction

import csv
import re

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

class Kickstarter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    desc = db.Column(db.String)
    category = db.Column(db.String)
    wanted = db.Integer
    pledged = db.Integer
    success = db.Float

    def __init__(self, id, title, desc, category, wanted, pledged, success):
        self.id = id
        self.title = title
        self.desc = desc
        self.category = category
        self.wanted = wanted
        self.pledged = pledged
        self.success = success

#db.create_all()

@app.route('/')
def index():
    return {'Hello': 'World!'}

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
        return {
            'exception': e
        }, 400

def similar(submission, dataset):
    # For now just take the first 5
    return [dataset[:5]]

def getchance(similardata):
    return 50

@app.route('/api/idea', methods=['HEAD', 'POST'])
def idea():
    if not request.is_json:
        return {'error': 'invalid submission'}, 400
    submission = request.get_json()
    def callback(session):
        dataset = session.query(Kickstarter).filter(Kickstarter.category==submission['category']).limit(200).all()
        similardata = similar(submission, dataset)
        return {
            'chance': getchance(similardata),
            'similar': [{
                'title': x[1],
                'url': '',
                'goal': x[4],
                'pledged': x[5]
            } for x in similardata]
        }
    return run_transaction(sessionmaker, callback)

#@app.route('/db/userideas')
def dbroute():
    def callback(session):
        return jsonify(session.query(UserIdea).all())
    return run_transaction(sessionmaker, callback)

@app.route('/db/kickstarter')
def kickstarterroute():
    def callback(session):
        data = session.query(Kickstarter).all()
        return {
            'count': len(data),
            'data': data
        }
    return run_transaction(sessionmaker, callback)

@app.route('/db/categories')
def categories():
    def callback(session):
        return jsonify([x[0] for x in session.query(Kickstarter.category).distinct().all()])
    return run_transaction(sessionmaker, callback)

@app.route('/db/loaddata')
def loaddata():
    data = []
    with open('ks-projects-201801.csv') as f:
        reader = csv.reader(f)
        # skip first row
        next(reader)

        for row in reader:
            newdata = {
                'id': row[0],
                'title': row[1],
                'desc': '',
                'category': row[3],
                'wanted': float(row[6]),
                'pledged': float(row[8]),
            }
            
            title = newdata['title']
            title = title.lower()
            title = re.sub('[^\w \']', ' ', title)
            title = re.sub('\s+', ' ', title)
            title = title.strip()
            newdata['title'] = title
            newdata['success'] = newdata['pledged']/newdata['wanted']
            data.append(newdata)
            def callback(session):
                session.add(Kickstarter(**newdata))
            run_transaction(sessionmaker, callback)
    return jsonify(data)

if __name__ == "__main__":
    app.run()
