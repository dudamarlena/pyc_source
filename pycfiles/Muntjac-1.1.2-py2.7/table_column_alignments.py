# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/table/table_column_alignments.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.test.server.component.table.table_generator import TableGenerator
from muntjac.ui.table import Table

class TableColumnAlignments(TestCase):

    def testDefaultColumnAlignments(self):
        for properties in range(10):
            t = TableGenerator.createTableWithDefaultContainer(properties, 10)
            expected = [None] * properties
            for i in range(properties):
                expected[i] = Table.ALIGN_LEFT

            self.assertEquals(expected, t.getColumnAlignments(), 'getColumnAlignments')

        return

    def testExplicitColumnAlignments(self):
        properties = 5
        t = TableGenerator.createTableWithDefaultContainer(properties, 10)
        explicitAlignments = [Table.ALIGN_CENTER, Table.ALIGN_LEFT,
         Table.ALIGN_RIGHT, Table.ALIGN_RIGHT, Table.ALIGN_LEFT]
        t.setColumnAlignments(explicitAlignments)
        self.assertEquals(explicitAlignments, t.getColumnAlignments(), 'Explicit visible columns, 5 properties')

    def testInvalidColumnAlignmentStrings(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT,
         Table.ALIGN_LEFT]
        try:
            t.setColumnAlignments(['a', 'b', 'c'])
            self.fail('No exception thrown for invalid array length')
        except ValueError:
            pass

        self.assertEquals(defaultAlignments, t.getColumnAlignments(), 'Invalid change affected alignments')

    def testInvalidColumnAlignmentString(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT,
         Table.ALIGN_LEFT]
        try:
            t.setColumnAlignment('Property 1', 'a')
            self.fail('No exception thrown for invalid array length')
        except ValueError:
            pass

        self.assertEquals(defaultAlignments, t.getColumnAlignments(), 'Invalid change affected alignments')

    def testColumnAlignmentForPropertyNotInContainer(self):
        t = TableGenerator.createTableWithDefaultContainer(3, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT,
         Table.ALIGN_LEFT]
        try:
            t.setColumnAlignment('Property 1200', Table.ALIGN_LEFT)
        except ValueError:
            pass

        self.assertEquals(defaultAlignments, t.getColumnAlignments(), 'Invalid change affected alignments')

    def testInvalidColumnAlignmentsLength(self):
        t = TableGenerator.createTableWithDefaultContainer(7, 7)
        defaultAlignments = [Table.ALIGN_LEFT, Table.ALIGN_LEFT,
         Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT,
         Table.ALIGN_LEFT, Table.ALIGN_LEFT]
        try:
            t.setColumnAlignments([Table.ALIGN_LEFT])
            self.fail('No exception thrown for invalid array length')
        except ValueError:
            pass

        self.assertEquals(defaultAlignments, t.getColumnAlignments(), 'Invalid change affected alignments')
        try:
            t.setColumnAlignments([])
            self.fail('No exception thrown for invalid array length')
        except ValueError:
            pass

        self.assertEquals(defaultAlignments, t.getColumnAlignments(), 'Invalid change affected alignments')
        try:
            t.setColumnAlignments([Table.ALIGN_LEFT, Table.ALIGN_LEFT,
             Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT,
             Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT])
            self.fail('No exception thrown for invalid array length')
        except ValueError:
            pass

        self.assertEquals(defaultAlignments, t.getColumnAlignments(), 'Invalid change affected alignments')

    def testExplicitColumnAlignmentOneByOne(self):
        properties = 5
        t = TableGenerator.createTableWithDefaultContainer(properties, 10)
        explicitAlignments = [Table.ALIGN_CENTER, Table.ALIGN_LEFT,
         Table.ALIGN_RIGHT, Table.ALIGN_RIGHT, Table.ALIGN_LEFT]
        currentAlignments = [
         Table.ALIGN_LEFT, Table.ALIGN_LEFT,
         Table.ALIGN_LEFT, Table.ALIGN_LEFT, Table.ALIGN_LEFT]
        for i in range(properties):
            t.setColumnAlignment('Property %d' % i, explicitAlignments[i])
            currentAlignments[i] = explicitAlignments[i]
            self.assertEquals(currentAlignments, t.getColumnAlignments(), 'Explicit visible columns, %d alignments set' % i)