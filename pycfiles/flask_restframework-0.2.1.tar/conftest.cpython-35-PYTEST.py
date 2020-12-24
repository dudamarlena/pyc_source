# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/tests/conftest.py
# Compiled at: 2017-06-30 11:16:28
# Size of source mod 2**32: 555 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from flask.app import Flask
from flask.ext.mongoengine import MongoEngine

@pytest.fixture()
def app():
    app = Flask(__name__)
    with app.app_context():
        yield app


@pytest.fixture()
def db(app):
    db = MongoEngine(app, config=dict(MONGODB_DB='test'))
    with app.app_context():
        database = db.connection.get_database('test')
        for col in database.collection_names():
            if col != 'system.indexes':
                print(col)
                database.drop_collection(col)

    return db