# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/thijs.dezoete/projects/mysql-statsd/mysql_statsd/preprocessors/columns_preprocessor.py
# Compiled at: 2015-02-24 09:56:17
from interface import Preprocessor

class ColumnsPreprocessor(Preprocessor):
    """Preprocessor for data returned in single row/multiple columns format (f.e.: SHOW SLAVE STATUS)"""

    def __init__(self, *args, **kwargs):
        super(ColumnsPreprocessor, self).__init__(*args, **kwargs)

    def process(self, rows, column_names):
        if not rows:
            return []
        return zip(column_names, rows[0])