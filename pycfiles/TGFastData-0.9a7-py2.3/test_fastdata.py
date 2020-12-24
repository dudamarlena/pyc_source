# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgfastdata\tests\test_fastdata.py
# Compiled at: 2007-07-14 11:29:05
from sqlobject import SQLObject, StringCol, IntCol, connectionForURI
from tgfastdata.datawidgets import FastDataGrid

class FakeUser(SQLObject):
    __module__ = __name__
    _connection = connectionForURI('sqlite:///:memory:')
    userId = IntCol()
    name = StringCol()

    def _get_displayName(self):
        return self.name.capitalize()


FakeUser.createTable()

class TestFastDataGrid:
    __module__ = __name__

    def setup(self):
        self.grid = FastDataGrid(template='tgfastdata.templates.datagrid')

    def test_dynamic_fields(self):
        fields = ['userId', 'displayName', ('Name', FakeUser._get_displayName), ('Name', 'displayName')]
        sr = FakeUser.select()
        d = dict(value=sr, fields=fields)
        self.grid.update_params(d)
        get_field = d['get_field']
        assert ['userId', 'displayName', 'column-2', 'column-3'] == d['collist']
        row = FakeUser(userId=123, name='john')
        assert 123 == get_field(row, 'userId')
        assert 'John' == get_field(row, 'displayName')
        assert 'John' == get_field(row, 'column-2')
        assert 'John' == get_field(row, 'column-3')

    def test_derive_fields_from_sr(self):
        sr = FakeUser.select()
        d = dict(value=sr)
        self.grid.update_params(d)
        get_field = d['get_field']
        assert ['userId', 'name'] == d['collist']
        row = FakeUser(userId=123, name='john')
        assert 123 == get_field(row, 'userId')
        assert 'john' == get_field(row, 'name')