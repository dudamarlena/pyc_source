# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\lib\GridEditor.py
# Compiled at: 2019-04-19 01:10:52
import wx, wx.xrc, wx.grid as gridlib, wx.dataview, copy

class TableGrid(gridlib.Grid):

    def __init__(self, parent, log):
        gridlib.Grid.__init__(self, parent, -1)
        self.table = DataTable(log)
        self.SetTable(self.table, True)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick)
        self.SetColSize(0, 200)
        self.SetColSize(1, 100)
        self.SetColSize(2, 300)
        self.SetColSize(3, 100)
        self.selRow = 0
        self.selCol = 0
        self.log = log

    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()
        evt.Skip()

    def OnLeftClick(self, evt):
        self.selRow = evt.GetRow()
        self.selCol = evt.GetCol()
        evt.Skip()

    def SetChoice(self, col, lt):
        self.table.SetChoice(col, lt)

    def DelRow(self):
        self.table.DeleteRows(self.selRow, 1)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.Update()
        return self.selRow

    def DelAll(self):
        self.table.DeleteAll()
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.Update()
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)

    def AddRow(self):
        self.table.AppendRows(1)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.Update()
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)

    def AddRows(self, numRows):
        self.table.AppendRows(numRows)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.Update()
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)

    def InsertRow(self, pos):
        self.table.InsertRows(pos, 1)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.Update()
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)

    def Refresh(self):
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.Update()
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)

    def Render(self, data):
        self.DelAll()
        self.AddRows(len(data))
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                self.table.SetValue(i, j, data[i][j])

        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.Update()
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)


class DataTable(gridlib.GridTableBase):

    def __init__(self, log):
        gridlib.GridTableBase.__init__(self)
        self.log = log
        self.colLabels = [
         'Name', 'Datatype', 'Comment', 'Init Value']
        self.dataTypes = [
         gridlib.GRID_VALUE_STRING,
         gridlib.GRID_VALUE_STRING,
         gridlib.GRID_VALUE_STRING,
         gridlib.GRID_VALUE_STRING]
        self.data = []
        self.itemdata = []
        self.defaultdata = [
         '', '', '', '']

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.colLabels)

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def GetItemValue(self, row, col):
        try:
            return self.itemdata[row][col]
        except IndexError:
            return

        return

    def SetValue(self, row, col, value):

        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)
                msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                self.GetView().ProcessTableMessage(msg)

        innerSetValue(row, col, value)

    def SetItemValue(self, row, col, value):

        def innerSetItemValue(row, col, value):
            try:
                self.itemdata[row][col] = value
            except IndexError:
                self.data.append([''] * self.GetNumberCols())
                innerSetItemValue(row, col, value)
                msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                self.GetView().ProcessTableMessage(msg)

        innerSetItemValue(row, col, value)

    def SetChoice(self, col, lt):
        self.dataTypes[col] = gridlib.GRID_VALUE_CHOICE + ':' + (',').join(lt)

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)

    def DeleteRows(self, pos=0, numRows=1):
        if pos > len(self.data) and pos < 0:
            return
        for i in range(0, numRows):
            del self.data[pos + i]
            del self.itemdata[pos + i]

        msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, pos, numRows)
        self.GetView().ProcessTableMessage(msg)

    def DeleteAll(self):
        nn = self.GetNumberRows()
        msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, 0, self.GetNumberRows())
        self.GetView().ProcessTableMessage(msg)
        self.data = []
        self.itemdata = []

    def AppendRows(self, numRows=1):
        for i in range(0, numRows):
            dd = copy.deepcopy(self.defaultdata)
            self.data.append(dd)
            dd2 = [None] * len(self.defaultdata)
            self.itemdata.append(dd2)

        msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, numRows)
        self.GetView().ProcessTableMessage(msg)
        return

    def InsertRows(self, pos, numRows=1):
        for i in range(0, numRows):
            dd = copy.deepcopy(self.defaultdata)
            self.data.insert(pos, dd)
            dd2 = [None] * len(self.defaultdata)
            self.itemdata.append(dd2)

        msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_INSERTED, pos, numRows)
        self.GetView().ProcessTableMessage(msg)
        return