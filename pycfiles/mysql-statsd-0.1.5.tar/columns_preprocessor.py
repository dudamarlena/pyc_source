# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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