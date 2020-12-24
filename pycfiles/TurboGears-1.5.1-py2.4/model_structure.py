# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\tests\catwalk_models\model_structure.py
# Compiled at: 2011-07-14 06:38:37
from sqlobject import SQLObject, StringCol, IntCol, connectionForURI
__connection__ = connectionForURI('sqlite:///:memory:')
hub = __connection__

class StringTest(SQLObject):
    __module__ = __name__
    name = StringCol(title='This is a title', length=200, default='new name')


StringTest.createTable(ifNotExists=True)

class NumTest(SQLObject):
    __module__ = __name__
    an_integer = IntCol(title='This is an integer', default=123)


NumTest.createTable(ifNotExists=True)