# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/postpy/connections.py
# Compiled at: 2016-12-26 16:36:55
# Size of source mod 2**32: 564 bytes
import os, psycopg2
__all__ = ('connect', )

def connect(host=None, database=None, user=None, password=None, **kwargs):
    """Create a database connection."""
    host = host or os.environ['PGHOST']
    database = database or os.environ['PGDATABASE']
    user = user or os.environ['PGUSER']
    password = password or os.environ['PGPASSWORD']
    return psycopg2.connect(host=host, database=database, user=user, password=password, **kwargs)