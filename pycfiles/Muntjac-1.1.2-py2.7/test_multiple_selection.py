# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/table/test_multiple_selection.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.table import Table
from muntjac.ui.abstract_select import MultiSelectMode
from muntjac.data.util.indexed_container import IndexedContainer

class TestMultipleSelection(TestCase):

    def testSetMultipleItems(self):
        """Tests weather the multiple select mode is set when using
        Table.set"""
        table = Table('', self.createTestContainer())
        table.setMultiSelect(True)
        self.assertTrue(table.isMultiSelect())
        table.setValue(['1', '3'])
        self.assertEquals(2, len(table.getValue()))

    def testSetMultiSelectMode(self):
        """Tests setting the multiselect mode of the Table. The multiselect
        mode affects how mouse selection is made in the table by the user.
        """
        table = Table('', self.createTestContainer())
        self.assertEquals(MultiSelectMode.DEFAULT, table.getMultiSelectMode())
        table.setMultiSelectMode(MultiSelectMode.SIMPLE)
        self.assertEquals(MultiSelectMode.SIMPLE, table.getMultiSelectMode())

    def createTestContainer(self):
        """Creates a testing container for the tests

        @return: A new container with test items
        """
        container = IndexedContainer(['1', '2', '3', '4'])
        return container