# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\tests\catwalk_models\model_list.py
# Compiled at: 2011-07-14 06:38:44
from sqlobject import SQLObject, StringCol, connectionForURI
__connection__ = connectionForURI('sqlite:///:memory:')
hub = __connection__

class FirstClass(SQLObject):
    __module__ = __name__
    name = StringCol(title='This is a title', length=200, default='new name')


class SecondClass(SQLObject):
    __module__ = __name__
    name = StringCol()


class ThirdClass(SQLObject):
    __module__ = __name__
    name = StringCol()


FirstClass.createTable(ifNotExists=True)
SecondClass.createTable(ifNotExists=True)
ThirdClass.createTable(ifNotExists=True)