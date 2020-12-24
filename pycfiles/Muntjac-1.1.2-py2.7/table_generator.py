# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/table/table_generator.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.table import Table

class TableGenerator(TestCase):

    @classmethod
    def createTableWithDefaultContainer(cls, properties, items):
        t = Table()
        for i in range(properties):
            t.addContainerProperty('Property %d' % i, str, None)

        for j in range(items):
            item = t.addItem('Item %d' % j)
            for i in range(properties):
                v = 'Item %d/Property %d' % (j, i)
                item.getItemProperty('Property %d' % i).setValue(v)

        return t

    def testTableGenerator(self):
        t = self.createTableWithDefaultContainer(1, 1)
        self.assertEquals(len(t), 1)
        self.assertEquals(len(t.getContainerPropertyIds()), 1)
        t = self.createTableWithDefaultContainer(100, 50)
        self.assertEquals(len(t), 50)
        self.assertEquals(len(t.getContainerPropertyIds()), 100)