# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/logservice/log.py
# Compiled at: 2016-09-10 09:34:50
# Size of source mod 2**32: 423 bytes
from .base import Base
from .models.log import Log as LogModel

class Log(Base):

    def get_collection(self, queryables=None):
        if queryables:
            items = self.dbsession.query(LogModel).filter_by(**queryables).all()
        else:
            items = self.dbsession.query(LogModel).all()
        return items

    def get(self, id):
        item = self.dbsession.query(LogModel).get(id)
        return item