# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/tests/dummy_site/app.py
# Compiled at: 2019-12-27 17:10:08
# Size of source mod 2**32: 316 bytes
from flask import Flask
from . import _index, movie, music

def create_app():
    app = Flask(__name__)
    app.register_blueprint(_index.bp)
    app.register_blueprint((movie.bp), url_prefix='/movie')
    app.register_blueprint((music.bp), url_prefix='/music')
    return app