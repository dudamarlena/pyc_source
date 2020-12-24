# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test.py
# Compiled at: 2015-10-31 08:41:56
from printtable import PrintTable
table = PrintTable(['name', 'old'])
table.append_data(name='Jack', old='20')
table.append_data(name=['Jack', 'Mary'], old=['20', '19'])
table.append_data_list(['Jack', '20'])
print 'The table with line number\n'
table.printTable(1)
print 'The table without line number\n'
table.printTable()