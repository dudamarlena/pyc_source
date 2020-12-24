# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgfastdata\tests\test_formmaker.py
# Compiled at: 2007-07-14 11:29:05
from turbogears.testutil import DBTest
import formencode
from tgfastdata import formmaker
from turbogears import validators
from turbogears import widgets
import formmodel

class TestSQLObjectWidgets(DBTest):
    __module__ = __name__
    model = formmodel

    def test_simpleWidgets(self):
        fields = formmaker.fields_for(formmodel.Person)
        assert len(fields) == 7
        assert fields[1].name == 'age'
        assert fields[1].default == 30
        assert isinstance(fields[1].validator, validators.Int)
        assert fields[0].label == 'Full Name'
        assert isinstance(fields[2], widgets.CalendarDatePicker)
        assert fields[3].name == 'friends'
        assert isinstance(fields[3].validator, formencode.ForEach)
        assert fields[4].name == 'company'
        assert len(fields[4].options) > 0
        assert fields[5].name == 'status'
        assert isinstance(fields[5], widgets.SingleSelectField)
        assert isinstance(fields[5].validator, validators.OneOf)
        assert fields[6].name == 'salary'
        assert isinstance(fields[6].validator, validators.Number)

    def test_inheritable_so(self):
        fields = formmaker.fields_for(formmodel.ChildSO)
        assert len(fields) == 2


ltests = (
 (
  'first_name', 'First Name'), ('firstName', 'First Name'), ('ADDRESS1', 'Address1'), ('email', 'Email'), ('secureID', 'Secure Id'), ('PhoneNO', 'Phone No'), ('floor1id', 'Floor1id'))
for ltest in ltests:
    assert formmaker.name2label(ltest[0]) == ltest[1]