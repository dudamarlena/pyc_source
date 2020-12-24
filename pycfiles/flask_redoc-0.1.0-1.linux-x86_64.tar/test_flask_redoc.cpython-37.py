# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mzaglia/workspace/flask-redoc/venv/lib/python3.7/site-packages/tests/flask_redoc_tests/test_flask_redoc.py
# Compiled at: 2020-03-13 09:27:42
# Size of source mod 2**32: 502 bytes
import pytest
from flask import Flask
from flask_redoc import Redoc

class TestFlaskRedoc:

    def test_redoc_yml(self):
        app = Flask(__name__)
        client = app.test_client()
        Redoc('petstore.yml', app)
        resp = client.get('/docs')
        assert resp.status_code == 200

    def test_redoc_json(self):
        app = Flask(__name__)
        client = app.test_client()
        Redoc('petstore.json', app)
        resp = client.get('/docs')
        assert resp.status_code == 200