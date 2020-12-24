# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muatik/projects/flask-profiler/flask_profiler/storage/base.py
# Compiled at: 2015-10-13 07:26:29


class BaseStorage(object):
    """docstring for BaseStorage"""

    def __init__(self):
        super(BaseStorage, self).__init__()

    def filter(self, criteria):
        raise Exception('Not implemneted Error')

    def getSummary(self, criteria):
        raise Exception('Not implemneted Error')

    def insert(self, measurement):
        raise Exception('Not implemented Error')

    def delete(self, measurementId):
        raise Exception('Not imlemented Error')