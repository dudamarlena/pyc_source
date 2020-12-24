# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\tests\catwalk_models\single_join.py
# Compiled at: 2011-03-26 09:20:13
from sqlobject import *
__connection__ = connectionForURI('sqlite:///:memory:')
hub = __connection__

class Client(SQLObject):
    __module__ = __name__
    name = StringCol()
    physical_address = SingleJoin('Address')


class Address(SQLObject):
    __module__ = __name__
    client = ForeignKey('Client', default=None)
    street = StringCol()


Client.createTable(ifNotExists=True)
Address.createTable(ifNotExists=True)