# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/table/test_footer.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.table import Table
from muntjac.data.util.indexed_container import IndexedContainer

class TestFooter(TestCase):
    """Test case for testing the footer API"""

    def testFooterVisibility(self):
        """Tests if setting the footer visibility works properly"""
        table = Table('Test table', self.createContainer())
        self.assertFalse(table.isFooterVisible())
        table.setFooterVisible(True)
        self.assertTrue(table.isFooterVisible())

    def testAddingFooters(self):
        """Tests adding footers to the columns"""
        table = Table('Test table', self.createContainer())
        self.assertIsNone(table.getColumnFooter('col1'))
        self.assertIsNone(table.getColumnFooter('col2'))
        self.assertIsNone(table.getColumnFooter('col3'))
        table.setColumnFooter('col1', 'Footer1')
        self.assertEquals('Footer1', table.getColumnFooter('col1'))
        table.setColumnFooter('col2', 'Footer2')
        self.assertEquals('Footer2', table.getColumnFooter('col2'))
        table.setColumnFooter('fail', 'FooterFail')

    def testRemovingFooters(self):
        """Test removing footers"""
        table = Table('Test table', self.createContainer())
        table.setColumnFooter('col1', 'Footer1')
        table.setColumnFooter('col2', 'Footer2')
        self.assertNotEquals(table.getColumnFooter('col1'), None)
        table.setColumnFooter('col1', None)
        self.assertEquals(table.getColumnFooter('col1'), None)
        self.assertNotEquals(table.getColumnFooter('col2'), None)
        table.setColumnFooter('fail', None)
        return

    @classmethod
    def createContainer(cls):
        """Creates a container with three properties "col1,col2,col3"
        with 100 items

        @return: Returns the created table
        """
        container = IndexedContainer()
        container.addContainerProperty('col1', str, '')
        container.addContainerProperty('col2', str, '')
        container.addContainerProperty('col3', str, '')
        for i in range(100):
            item = container.addItem('item %d' % i)
            item.getItemProperty('col1').setValue('first%d' % i)
            item.getItemProperty('col2').setValue('middle%d' % i)
            item.getItemProperty('col3').setValue('last%d' % i)

        return container