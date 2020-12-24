# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thijs.dezoete/projects/mysql-statsd/mysql_statsd/preprocessors/interface.py
# Compiled at: 2014-08-08 08:30:13


class Preprocessor(object):

    def process(self, rows):
        """ Can do preprocessing on rows if needed for different
            database types """
        return rows