# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/sqlite.py
# Compiled at: 2018-04-20 03:19:42
import re, sqlite3
try:
    import sqlparse

    def is_read_only_query(query):
        statements = sqlparse.parse(query)
        for statement in statements:
            if statement.get_type() != 'SELECT':
                return False

        return True


except ImportError:

    def is_read_only_query(query):
        if re.match('select ', query, re.IGNORECASE):
            if re.search('^([^"]|"[^"]*")*?;', query) or re.search("^([^']|'[^']*')*?;", query):
                return False
            return True
        return False


def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection