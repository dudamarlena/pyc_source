# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\soccer\soccer.py
# Compiled at: 2017-09-06 14:19:22
# Size of source mod 2**32: 474 bytes
""" Central class for the soccer data api. """
from soccer.data_connectors import FDOConnector, SQLiteConnector

class Soccer(object):
    __doc__ = '\n    Central class for the soccer data api.\n    '

    def __init__(self, fd_apikey=None, db_path=None):
        self.fdo = FDOConnector(fd_apikey)
        self.db = SQLiteConnector(db_path)
        season = self.get_current_season()

    def get_current_season(self):
        self.fdo.get_current_season()