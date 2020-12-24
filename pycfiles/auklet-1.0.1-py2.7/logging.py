# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/auklet/monitoring/logging.py
# Compiled at: 2018-10-16 12:42:27


class AukletLogging(object):

    def log(self, msg, data_type, level='INFO'):
        raise NotImplementedError('Must implement method: log')

    def debug(self, msg, data_type):
        self.log(msg, data_type, 'DEBUG')

    def info(self, msg, data_type):
        self.log(msg, data_type, 'INFO')

    def warning(self, msg, data_type):
        self.log(msg, data_type, 'WARNING')

    def error(self, msg, data_type):
        self.log(msg, data_type, 'ERROR')

    def critical(self, msg, data_type):
        self.log(msg, data_type, 'CRITICAL')