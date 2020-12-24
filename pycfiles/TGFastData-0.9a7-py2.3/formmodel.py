# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgfastdata\tests\formmodel.py
# Compiled at: 2007-07-14 11:29:05
from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject
from turbogears.database import PackageHub
hub = PackageHub('turbogears.widgets.tests.formmodel')
__connection__ = hub

class Person(SQLObject):
    __module__ = __name__
    form_order = [
     'name', 'age', 'date', 'friends', 'company', 'status', 'salary']
    name = StringCol(title='Full Name')
    age = IntCol(default=30)
    date = DateCol()
    friends = RelatedJoin('Person', otherColumn='friend_id')
    company = ForeignKey('Company', title='Company', default=None)
    status = EnumCol(enumValues=['Employed', 'Unemployed'], default='Unemployed', title='Status')
    salary = FloatCol()

    def __unicode__(self):
        return unicode(self.name)


class Company(SQLObject):
    __module__ = __name__
    name = UnicodeCol(title='Company name')
    employees = MultipleJoin('Person')

    def __unicode__(self):
        return self.name


class TestStringColWithTitle(SQLObject):
    """ Test model for ticket #272 and #300 """
    __module__ = __name__
    name = StringCol(title='This is the name')
    age = IntCol(title='Edad')


class BaseSO(InheritableSQLObject):
    __module__ = __name__
    parent_col = StringCol()


class ChildSO(BaseSO):
    __module__ = __name__
    child_col = StringCol()