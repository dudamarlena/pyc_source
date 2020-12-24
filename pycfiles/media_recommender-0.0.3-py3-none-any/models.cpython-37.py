# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\fyp-media-recommender\mediarecommender\recommender\models.py
# Compiled at: 2019-04-07 17:51:01
# Size of source mod 2**32: 1364 bytes
from mediarecommender.recommender import db

class Movie(db.Model):
    id = db.Column((db.Integer), primary_key=True)
    imdb_id = db.Column((db.Integer), nullable=False)
    title = db.Column((db.String()), nullable=False)
    genres = db.Column((db.String()), nullable=False)
    rating = db.Column((db.Float()), nullable=False)
    url = db.Column((db.String()), nullable=False)
    vector = db.Column((db.String()), nullable=False)

    def __repr__(self):
        return f"Movie({self.id}, '{self.title}', '{self.kind}')"


class Game(db.Model):
    id = db.Column((db.Integer), primary_key=True)
    steam_id = db.Column((db.Integer), nullable=False)
    title = db.Column((db.String()), nullable=False)
    rating = db.Column((db.Float()), nullable=False)
    url = db.Column((db.String()), nullable=False)
    vector = db.Column((db.String()), nullable=False)

    def __repr__(self):
        return f"Game({self.id}, '{self.title}')"


class Book(db.Model):
    id = db.Column((db.Integer), primary_key=True)
    goodreads_id = db.Column((db.Integer), nullable=False)
    title = db.Column((db.String()), nullable=False)
    rating = db.Column((db.Float()), nullable=False)
    url = db.Column((db.String()), nullable=False)
    vector = db.Column((db.String()), nullable=False)

    def __repr__(self):
        return f"Book({self.id}, '{self.title}')"