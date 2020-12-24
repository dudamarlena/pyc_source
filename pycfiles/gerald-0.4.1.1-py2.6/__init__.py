# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gerald/__init__.py
# Compiled at: 2010-10-31 02:23:23
"""
Gerald is a general purpose toolkit for managing and deploying database 
schemas. Its major current use is to identify the differences between 
various versions of a schema.

For more information see the web site at U{http://halfcooked.com/code/gerald}
"""
__version__ = (0, 4, 1, 1)
try:
    from oracle_schema import Schema as OracleSchema
except ImportError:
    pass

try:
    from mysql_schema import Schema as MySQLSchema
except ImportError:
    pass

try:
    from postgres_schema import Schema as PostgresSchema
except ImportError:
    pass