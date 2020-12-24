# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/zeg/sql.py
# Compiled at: 2018-04-18 10:54:17
# Size of source mod 2**32: 424 bytes
"""SQL driver wrappers."""
try:
    import sqlalchemy
except ImportError:
    have_driver = False
else:
    have_driver = True

def create_engine(conn_str, verbose):
    """Give engine from url connection string."""
    return sqlalchemy.create_engine(conn_str, echo=verbose)


def create_statement(query_str):
    """Give statement from string query."""
    return sqlalchemy.text(query_str)