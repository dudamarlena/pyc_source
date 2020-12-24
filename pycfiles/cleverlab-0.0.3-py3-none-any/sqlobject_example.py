# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/project/+package+/models/sqlobject_example.py
# Compiled at: 2006-08-02 05:57:51
from sqlobject import *

class Person(SQLObject):
    __module__ = __name__
    firstName = StringCol()
    middleInitial = StringCol(length=1, default=None)
    lastName = StringCol()
    addresses = MultipleJoin('Address')
    roles = RelatedJoin('Role')


class Address(SQLObject):
    __module__ = __name__
    street = StringCol()
    city = StringCol()
    state = StringCol(length=2)
    zip = StringCol(length=9)
    person = ForeignKey('Person')


class Role(SQLObject):
    __module__ = __name__
    name = StringCol(alternateID=True, length=20)
    persons = RelatedJoin('Person')