# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/empty_tree_table.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.tree_table import TreeTable

class EmptyTreeTable(TestCase):

    def testLastId(self):
        treeTable = TreeTable()
        self.assertFalse(treeTable.isLastId(treeTable.getValue()))