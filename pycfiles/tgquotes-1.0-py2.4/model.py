# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgquotes\model.py
# Compiled at: 2006-12-11 14:54:35
from sqlobject import *
from turbogears.database import PackageHub
import random
hub = PackageHub('tgquotes')
__connection__ = hub

class Quote(SQLObject):
    __module__ = __name__
    quote = UnicodeCol(notNone=True)

    @classmethod
    def random(cls, num=1):
        """
        Returns $num quotes, selected at random, or all of the quotes if num is larger.
        """
        if num > Quote.select().count():
            return list(Quote.select())
        else:
            return random.sample(list(Quote.select()), num)