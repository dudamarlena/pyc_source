# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_chi.py
# Compiled at: 2015-11-02 07:35:18
from printtable import PrintTable
table = PrintTable(['name', 'old'])
table.append_data(name='小明', old='20')
table.append_data(name=['小华', '大傻'], old=['20', '19'])
table.append_data_list(['二傻子', '20'])
print 'The table with line number\n'
table.printTable(1)
print 'The table without line number\n'
table.printTable()