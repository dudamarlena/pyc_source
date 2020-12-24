# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/models/HalWebModels.py
# Compiled at: 2012-01-05 21:48:33
from google.appengine.ext import db

class Welcome(db.Model):
    """TODO: Describe Welcome"""

    @classmethod
    def CreateNew(cls, _isAutoInsert=False):
        result = cls()
        if _isAutoInsert:
            result.put()
        return result

    def __str__(self):
        return 'Change __str__ method'