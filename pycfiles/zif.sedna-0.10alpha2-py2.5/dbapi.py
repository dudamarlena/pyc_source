# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/sedna/dbapi.py
# Compiled at: 2008-03-30 11:18:23
from dbapiexceptions import Error, Warning, InterfaceError, DatabaseError, InternalError, OperationalError, ProgrammingError, IntegrityError, DataError, NotSupportedError
from protocol import SednaProtocol
try:
    from zope.rdb import parseDSN
except ImportError:
    from externals import parseDSN

apilevel = 2.0
threadsafety = 2
paramstyle = 'format'

def connect(dsn=None, host=None, database=None, username=None, password=None, port=5050, trace=False):
    """ we hope to have a dsn formatted like
        dbi://user:passwd@host:port/dbname
    """
    if dsn:
        conn_info = parseDSN(dsn)
    if conn_info['host']:
        host = conn_info['host']
    if conn_info['port']:
        port = int(conn_info['port'])
    if conn_info['username']:
        username = conn_info['username']
    if conn_info['password']:
        password = conn_info['password']
    if conn_info['dbname']:
        database = conn_info['dbname']
    return SednaProtocol(host, database, username, password, port, trace)