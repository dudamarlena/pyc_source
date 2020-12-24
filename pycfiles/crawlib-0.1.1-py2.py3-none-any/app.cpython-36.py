# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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