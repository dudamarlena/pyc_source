# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dbsync/models/peewee.py
# Compiled at: 2015-04-10 05:21:53
__author__ = 'nathan'
try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from peewee import *
except ImportError:
    raise ImportError('PeeweeModel requires peewee installed')

from dbsync.models.base import SyncBaseModel

class PeeweeModel(SyncBaseModel, Model):

    def __init__(self):
        pass

    @classmethod
    def data_size(cls):
        """
        Total table size, query from table status
        :return:
        """
        return cls._status()['Data_length']

    @classmethod
    def avg_row_size(cls):
        """
        avg size per row, query from table status
        :return:
        """
        return cls._status()['Avg_row_length']

    @classmethod
    def row_count(cls):
        """
        query by count(*)
        :return:
        """
        return cls.raw('select * from (?)', cls._meta.db_table)

    @classmethod
    def rows(cls):
        """
        query from table status
        :return:
        """
        return cls._status()['Rows']

    @classmethod
    def _status(cls):
        return cls.raw('show table status like "(table_name)" ', cls._meta.db_table).dicts.execute()