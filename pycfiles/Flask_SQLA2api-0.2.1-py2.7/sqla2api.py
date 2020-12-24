# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/flask_sqla2api/sqla2api.py
# Compiled at: 2018-01-27 10:57:45
from flask import request
from .models import Model

class SQLA2api(object):

    def __init__(self, models=None, db=None):
        self.db = None
        self.models = []
        if db is not None:
            self.init_db(db)
        if models is not None:
            self.init_models(models)
        return

    def init_models(self, models):
        self.models = []
        for model in models:
            self.models.append(Model(model, self.db))

    def init_db(self, db):
        self.db = db

    def append_blueprints(self, app):
        if app is None:
            raise ValueError('Cannot append to null app.')
        for model in self.models:
            app.register_blueprint(model.make_blueprint(), url_prefix='/')

        return


def generate_blueprint(model, db):
    model = Model(model, db)
    return model.make_blueprint()