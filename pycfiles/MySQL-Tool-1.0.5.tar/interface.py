# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/thijs.dezoete/projects/mysql-statsd/mysql_statsd/preprocessors/interface.py
# Compiled at: 2014-08-08 08:30:13


class Preprocessor(object):

    def process(self, rows):
        """ Can do preprocessing on rows if needed for different
            database types """
        return rows