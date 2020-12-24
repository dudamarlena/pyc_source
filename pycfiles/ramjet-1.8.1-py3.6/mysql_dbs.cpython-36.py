# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/models/mysql_dbs.py
# Compiled at: 2017-11-07 02:38:41
# Size of source mod 2**32: 396 bytes
from .base import BaseMySQLModel

def create_mysql_model(db_name):

    class Model(BaseMySQLModel):
        _db_name = db_name

    return Model


_models = {}

def get_mysql_model(db_name):
    if db_name in _models:
        model = _models[db_name]
    else:
        model = create_mysql_model(db_name)
        _models[db_name] = model
    return model


MovotoDB = get_mysql_model('movoto')