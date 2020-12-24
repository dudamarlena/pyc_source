# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dbsync/models/sqlalchemy.py
# Compiled at: 2015-04-10 05:21:53
__author__ = 'nathan'
try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from sqlalchemy import create_engine, Table, Column, MetaData, Unicode, Float, LargeBinary, select
    from sqlalchemy.exc import IntegrityError
except ImportError:
    raise ImportError('SQLAlchemyJobStore requires SQLAlchemy installed')

from dbsync.models.base import SyncBaseModel

class SQLAlchemyModel(SyncBaseModel, Table):
    pass