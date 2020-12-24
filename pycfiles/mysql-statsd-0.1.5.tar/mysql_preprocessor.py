# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thijs.dezoete/projects/mysql-statsd/mysql_statsd/preprocessors/mysql_preprocessor.py
# Compiled at: 2014-08-08 08:30:13
from interface import Preprocessor

class MysqlPreprocessor(Preprocessor):

    def __init__(self, *args, **kwargs):
        super(MysqlPreprocessor, self).__init__(*args, **kwargs)

    def process(self, rows):
        return list(rows)