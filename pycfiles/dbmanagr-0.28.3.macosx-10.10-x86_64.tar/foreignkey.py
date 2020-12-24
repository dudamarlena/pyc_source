# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/model/foreignkey.py
# Compiled at: 2015-10-11 07:17:06
from dbmanagr.jsonable import Jsonable

class ForeignKey(Jsonable):
    """A foreign key connection between the originating column a and the
foreign column b"""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '%s -> %s' % (self.a, self.b)