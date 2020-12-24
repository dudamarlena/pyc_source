# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mal/Dropbox/Python/cold-start-recommender/csrec/DALFactory.py
# Compiled at: 2015-08-29 14:13:14
__author__ = 'elegans.io Ltd'
__email__ = 'info@elegans.io'

def DALFactory(name='mem', **params):
    if name == 'mem':
        import MemDAL
        dal = MemDAL.Database()
    else:
        dal = None
    dal.init(**params)
    return dal