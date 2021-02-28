#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction

import csv
import re
from urllib.parse import quote
import string
from random import randrange

import bert

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
    __tablename__ = 'kickstarterdata'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    desc = db.Column(db.String)
    category = db.Column(db.String)
    wanted = db.Column(db.Float)
    pledged = db.Column(db.Float)
    success = db.Column(db.Float)

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
            'amount': 94.56,
            'similar': [
                    {
                        'title': yourtitle,
                        'url': 'https://example.com/your-request',
                        'category': 'category1',
                        'subcategory': 'subcat1',
                        'goal': 1,
                        'raised': 1
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
    titles = [x.title for x in dataset]
    indices = bert.data_processing(submission['title'], titles)
    return [dataset[i] for i in indices]

def getchance(similardata):
    chanceavg = sum([x.success for x in similardata])/len(similardata)
    return round(chanceavg*100, 2)

def getkickstarterjson(x):
    return {
        'title': string.capwords(str(x.title)),
        'url': 'https://www.kickstarter.com/discover/advanced?ref=nav_search&term='+quote(x.title),
        'category': x.category,
        'goal': x.wanted,
        'raised': x.pledged
    }

@app.route('/api/idea', methods=['HEAD', 'POST'])
def idea():
    if not request.is_json:
        return {'error': 'invalid submission'}, 400
    submission = request.get_json()
    def callback(session):
        dataset = session.query(Kickstarter).filter(Kickstarter.category==submission['category']).limit(200).all()
        similardata = similar(submission, dataset)
        chance =  getchance(similardata)
        return {
            'chance': min(chance, 99.99),
            'amount': round(float(submission['amount'])*(chance/100), 2),
            'similar': [getkickstarterjson(x) for x in similardata]
        }
    return run_transaction(sessionmaker, callback)

#@app.route('/db/userideas')
def dbroute():
    def callback(session):
        return jsonify(session.query(UserIdea).all())
    return run_transaction(sessionmaker, callback)

#@app.route('/db/kickstarter')
def kickstarterroute():
    def callback(session):
        data = session.query(Kickstarter).all()
        return {
            'count': len(data),
            'data': [getkickstarterjson(x) for x in data]
        }
    return run_transaction(sessionmaker, callback)

@app.route('/db/categories')
def categories():
    def callback(session):
        return jsonify([x[0] for x in session.query(Kickstarter.category).distinct().all()])
    return run_transaction(sessionmaker, callback)

#@app.route('/db/loaddata')
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
