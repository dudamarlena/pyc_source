# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/myams/table.py
# Compiled at: 2014-09-12 09:57:49
from z3c.table.table import Table

class BaseTable(Table):
    """Custom table"""
    data_attributes = {}
    batchSize = 10000
    startBatchingAt = 10000

    @staticmethod
    def checkDataAttribute(attribute, source):
        if isinstance(attribute, (str, unicode)):
            return attribute
        else:
            if callable(attribute):
                return attribute(source)
            return str(attribute)

    def getDataAttributes(self, element, source, column=None):
        attrs = self.data_attributes.get(element)
        if attrs:
            return (' ').join("%s='%s'" % (item[0], self.checkDataAttribute(item[1], source)) for item in attrs.iteritems())
        else:
            return ''

    def renderTable(self):
        return super(BaseTable, self).renderTable().replace('<table', '<table %s' % self.getDataAttributes('table', self))

    def renderRow(self, row, cssClass=None):
        return super(BaseTable, self).renderRow(row, cssClass).replace('<tr', '<tr %s' % self.getDataAttributes('tr', row[0][0]))

    def renderCell(self, item, column, colspan=0):
        return super(BaseTable, self).renderCell(item, column, colspan).replace('<td', '<td %s' % self.getDataAttributes('td', item, column))