# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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