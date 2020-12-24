# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/spackl/db/redshift.py
# Compiled at: 2019-03-08 14:26:50
"""
    Class for using Redshift as a source database
"""
from .postgres import Postgres

class Redshift(Postgres):
    _db_type = 'redshift+psycopg2'

    def __init__(self, *args, **kwargs):
        port = 5439
        if 'port' in kwargs:
            port = kwargs.pop('port')
        conn_params = {'sslmode': 'prefer'}
        super(Redshift, self).__init__(port=port, conn_params=conn_params, *args, **kwargs)