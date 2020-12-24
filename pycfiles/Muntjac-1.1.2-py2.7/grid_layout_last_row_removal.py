# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/components/grid_layout_last_row_removal.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.grid_layout import GridLayout
from muntjac.ui.label import Label

class TestGridLayoutLastRowRemoval(TestCase):

    def testRemovingLastRow(self):
        grid = GridLayout(2, 1)
        grid.addComponent(Label('Col1'))
        grid.addComponent(Label('Col2'))
        try:
            grid.removeRow(0)
        except ValueError:
            self.fail('removeRow(0) threw an ValueError when removing the last row')

        self.assertEquals(2, grid.getColumns())
        self.assertEquals(1, grid.getRows())
        self.assertEquals(grid.getComponent(0, 0), None, 'A component should not be left in the layout')
        self.assertEquals(grid.getComponent(1, 0), None, 'A component should not be left in the layout')
        self.assertEquals(0, grid.getCursorX())
        self.assertEquals(0, grid.getCursorY())
        return