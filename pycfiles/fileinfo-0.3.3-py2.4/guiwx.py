# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/guiwx.py
# Compiled at: 2008-06-07 18:21:40
import sys, wx, wx.grid as gridlib
from wx.lib.mixins.inspection import InspectableApp

class SimpleGrid(gridlib.Grid):
    __module__ = __name__

    def __init__(self, parent, log):
        gridlib.Grid.__init__(self, parent, -1)
        self.log = log
        self.moveTo = None
        return

    def doDisplay(self):
        for (y, row) in enumerate(self.TABLE + self.FOOTER):
            for (x, value) in enumerate(row):
                self.SetCellValue(y, x, str(value))
                self.SetReadOnly(y, x, True)

    def setMyTable(self, HEADER, TABLE, FOOTER):
        self.HEADER = HEADER
        self.TABLE = TABLE
        self.FOOTER = FOOTER
        self.CreateGrid(len(self.TABLE + self.FOOTER), len(self.HEADER))
        self.EnableEditing(False)
        self.EnableDragColSize()
        self.EnableDragColMove()
        self.DisableDragRowSize()
        self.SetSelectionMode(1)
        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
        for (i, title) in enumerate(self.HEADER):
            self.SetColLabelValue(i, title)

        self.doDisplay()
        attr1 = gridlib.GridCellAttr()
        attr1.SetBackgroundColour(wx.WHITE)
        attr2 = gridlib.GridCellAttr()
        lightBlue = wx.Colour(0.9294 * 255, 0.9529 * 255, 0.9961 * 255)
        attr2.SetBackgroundColour(lightBlue)
        for (y, row) in enumerate(TABLE):
            self.SetRowAttr(y, [attr1, attr2][(y % 2)])

        attr = gridlib.GridCellAttr()
        grey = wx.Colour(0.666667 * 255, 0.666667 * 255, 0.666667 * 255)
        attr.SetBackgroundColour(grey)
        self.SetRowAttr(len(self.TABLE + self.FOOTER) - 1, attr)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)

    def OnCellLeftClick(self, evt):
        row, col = evt.GetRow(), evt.GetCol()
        if row < len(self.TABLE):
            self.SelectRow(row, True)
            evt.Skip()

    def OnRangeSelect(self, evt):
        tl, br = evt.GetTopLeftCoords(), evt.GetBottomRightCoords()
        if br[0] < len(self.TABLE):
            evt.Skip()

    def OnLabelLeftClick(self, evt):
        col = evt.GetCol()
        if col >= 0:
            tab = []
            for (i, row) in enumerate(self.TABLE):
                tab.append([row[col]] + row + [1])

            tab.sort()
            self.TABLE = [ row[1:-1] for row in tab ]
            self.doDisplay()
            self.ForceRefresh()
            evt.Skip()

    def OnIdle(self, evt):
        if self.moveTo != None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None
        evt.Skip()
        return


class TestFrame(wx.Frame):
    __module__ = __name__

    def __init__(self, parent, log):
        wx.Frame.__init__(self, parent, -1, 'Table results', size=(500, 300))
        self.grid = SimpleGrid(self, log)


def main(HEADER, TABLE, FOOTER):
    app = InspectableApp(False)
    frame = TestFrame(None, sys.stdout)
    frame.grid.setMyTable(HEADER, TABLE, FOOTER)
    frame.Show(True)
    app.MainLoop()
    return


if __name__ == '__main__':
    pass