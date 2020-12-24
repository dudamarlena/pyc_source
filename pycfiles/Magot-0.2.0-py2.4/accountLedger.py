# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/magot/accountLedger.py
# Compiled at: 2006-09-09 20:13:48
import weakref, wx, wx.grid as gridlib
from magot.guiutil import *
from magot.refdata import *
from magot.model import Entry

def _getdata(col, entry):
    if col == 0:
        return entry.date
    if col == 1:
        return entry.number
    if col == 2:
        return entry.description
    if col == 3:
        return getattr(entry, 'oppositeAccount', entry.oppositeEntry.account)
    if col == 4:
        return entry.isReconciled
    if col == 5:
        if entry.isDebit:
            return entry.amount
        else:
            return Money.Zero
    if col == 6:
        if not entry.isDebit:
            return entry.amount
        else:
            return Money.Zero
    if col == 7:
        return entry.balance


def _setdata(col, entry, value=None):
    if col == 0:
        entry.date = value
    elif col == 1:
        entry.number = value
    elif col == 2:
        entry.description = value
    elif col == 3:
        entry.oppositeAccount = value
    elif col == 4:
        entry.isReconciled = value
    elif col == 5:
        entry.isDebit = True
        entry.amount = Money(value)
    elif col == 6:
        entry.isDebit = False
        entry.amount = Money(value)


class AccountLedgerModel(gridlib.PyGridTableBase):
    """ The MVC model containing all entries for an account.
        Synchronize automatically with the view to do sorting, updating, ...
    """
    __module__ = __name__

    def __init__(self, view, account, log):
        gridlib.PyGridTableBase.__init__(self)
        self.account = account
        self.log = log
        self.colLabels = ['Date', 'Num', 'Description', 'Opposite Account', 'R', 'Debit', 'Credit', 'Balance']
        self.dataTypes = [
         gridlib.GRID_VALUE_DATETIME, gridlib.GRID_VALUE_STRING, gridlib.GRID_VALUE_STRING, gridlib.GRID_VALUE_CHOICE, gridlib.GRID_VALUE_BOOL, 'MoneyRenderer', 'MoneyRenderer', 'MoneyRenderer']
        self.data = []

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.colLabels)

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        try:
            entry = self.GetEntry(row)
        except:
            print 'bad row', row
            return ''

        return _getdata(col, entry)

    def SetValue(self, row, col, value):
        try:
            if not self.GetView().HasEntryBeenModified():
                e = self.GetEntry(row)
                modifiedEntry = self.GetView().PrepareEntryForModification(e)
                self.SetEntry(row, modifiedEntry)
            _setdata(col, self.GetView().GetModifiedEntry(), value)
        except IndexError:
            self.data.append([''] * self.GetNumberCols())
            self.SetValue(row, col, value)
            msg = gridlib.GridTableMessage(self, gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
            self.GetView().ProcessTableMessage(msg)

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

    def GetEntry(self, row):
        if self.GetNumberRows() > 0:
            entry = self.data[row]
            return entry
        return

    def SetEntry(self, row, entry):
        self.data[row] = entry

    def GetRow(self, entry):
        entryIndex = self.data.index(entry)
        return entryIndex

    def RefreshModel(self, sortByCol=None, sortOrder=1, focusEntry=None, sync=True):
        if focusEntry is None:
            focusEntry = self.GetView().GetSelectedEntry()
        msg = 'Refresh called on ledger ' + self.account.name
        if focusEntry is None:
            msg += ' with no focus.\n'
        else:
            msg += " with focus on entry '" + focusEntry.description + "'\n"
        self.log.write(msg)
        if sync:
            self._syncModelAgainstAccount()
        if sortByCol is not None:
            self.Sort(updateView=False, byCol=sortByCol, descending=sortOrder == -1)
        msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.GetView().ProcessTableMessage(msg)
        self.GetView().ReleaseEntryForModification()
        if focusEntry:
            self.GetView().SetCursorOn(focusEntry.getOriginalObject())
        else:
            self.GetView().SetCursorOn(None)
        return

    def Sort(self, byCol=0, descending=False, updateView=True):
        self.log.write('Sort() called on ledger %s, column %d\n' % (self.account.name, byCol))
        if self.GetNumberRows() < 2:
            return
        if byCol == 0:
            self.data = list(self.account.entries)
            if descending:
                self.data.reverse()
        else:

            def keyColumn(col):
                return lambda entry: _getdata(col, entry)

            self.data.sort(key=keyColumn(byCol), reverse=descending)
        if updateView:
            msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
            self.GetView().ProcessTableMessage(msg)

    def _syncModelAgainstAccount(self):
        lo = self.GetNumberRows()
        self.data = list(self.account.entries)
        ln = len(self.data)
        if lo != ln:
            if ln > lo:
                msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, ln - lo)
            elif lo > ln:
                msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, 0, lo - ln)
        else:
            msg = None
        if msg is not None:
            self.GetView().ProcessTableMessage(msg)
        return


class AccountLedgerView(gridlib.Grid, GridCtrlAutoWidthMixin):
    """ It's a page of the notebook that displays all entries of an account. """
    __module__ = __name__

    def __init__(self, parent, account, log):
        super(AccountLedgerView, self).__init__(parent, -1)
        GridCtrlAutoWidthMixin.__init__(self)
        self.mainFrame = self.GetParent().GetParent().GetParent().GetParent()
        self.ctx = parent.ctx
        self.account = account
        events.subscribe(self.account.changedEvent, self.RefreshView)
        self.log = log
        self.sortByCol = 0
        self.sortOrder = 1
        table = AccountLedgerModel(self, account, log)
        self.SetTable(table, True)
        self.SetDefaultRowSize(20)
        self.SetRowLabelSize(0)
        self.SetSelectionBackground(colourLemonChiffon)
        self.SetSelectionForeground('Black')
        self.SetColSize(0, 80)
        attr = gridlib.GridCellAttr()
        attr.SetRenderer(gridlib.GridCellStringRenderer())
        attr.SetEditor(DateCellEditor(log))
        self.SetColAttr(0, attr)
        self.SetColSize(1, 50)
        self.SetColSize(2, 300)
        self.SetColSize(3, 230)
        attr = gridlib.GridCellAttr()
        attr.SetEditor(OppositeAccountEditor(self.ctx))
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
        self.SetColAttr(3, attr)
        self.SetColSize(4, 30)
        self.SetColSize(5, 100)
        attr = gridlib.GridCellAttr()
        attr.SetRenderer(MoneyRenderer())
        attr.SetEditor(MoneyEditor())
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
        self.SetColAttr(5, attr)
        self.SetColSize(6, 100)
        attr = gridlib.GridCellAttr()
        attr.SetRenderer(MoneyRenderer())
        attr.SetEditor(MoneyEditor())
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
        self.SetColAttr(6, attr)
        self.SetColSize(7, 100)
        attr = gridlib.GridCellAttr()
        attr.SetReadOnly(True)
        attr.SetRenderer(MoneyRenderer())
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
        self.SetColAttr(7, attr)
        self.__enableEdit = 0
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnSort)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)

    def GetTable(self):
        return self.tableRef()

    def SetTable(self, object, *attributes):
        self.tableRef = weakref.ref(object)
        return gridlib.Grid.SetTable(self, object, *attributes)

    def OnIdle(self, evt):
        if self.__enableEdit and self.GetGridCursorCol() != 0:
            if self.CanEnableCellControl():
                self.EnableCellEditControl()
            self.__enableEdit = 0
        evt.Skip()

    def OnSelectCell(self, evt):
        if self.IsCellEditControlEnabled():
            self.HideCellEditControl()
            self.DisableCellEditControl()
        if self.GetGridCursorRow() != evt.GetRow():
            if not self.CheckTransactionModification():
                return
        self.SelectRow(evt.GetRow())
        if self.isNotebookChanged():
            self.mainFrame.nb = self.GetParent()
        self.__enableEdit = 1
        evt.Skip()

    def isNotebookChanged(self):
        currentNotebook = self.GetParent()
        lastNotebook = self.mainFrame.nb
        return currentNotebook is not lastNotebook

    def OnKeyDown(self, evt):
        if evt.KeyCode() != wx.WXK_RETURN or evt.ControlDown():
            evt.Skip()
            return
        self.DisableCellEditControl()
        self.CheckTransactionModification(askConfirmation=False)
        evt.Skip()

    def OnSort(self, evt):
        if self.sortByCol == evt.GetCol():
            self.sortOrder = -self.sortOrder
        else:
            self.sortByCol = evt.GetCol()
        self.RefreshView(sync=False, sort=True)

    def OnRangeSelect(self, evt):
        if evt.Selecting() and evt.GetBottomRow() != evt.GetTopRow():
            evt.Veto()
            self.SelectRow(self.GetGridCursorRow())
        evt.Skip()

    def GetSelectedEntry(self):
        row = self.GetGridCursorRow()
        if row not in [None, -1]:
            selectedEntry = self.GetTable().GetEntry(row)
            return selectedEntry
        return

    def SetCursorOn(self, entry):
        try:
            row = self.GetTable().GetRow(entry)
        except ValueError:
            row = 0

        self.SetGridCursor(row, 0)
        self.MakeCellVisible(row, 0)

    def RefreshView(self, source=None, event=None, focusEntry=None, sync=True, sort=True):
        col = None
        if sort:
            col = self.sortByCol
        self.GetTable().RefreshModel(focusEntry=focusEntry, sync=sync, sortByCol=col, sortOrder=self.sortOrder)
        self.setAlternateColours(self.GetNumberRows(), self.GetNumberCols() - 3)
        return

    def setAlternateColours(self, rowNb, colNb):

        def setCellColour(firstCol, rowNb, colNb, colour):
            setCellColour = self.SetCellBackgroundColour
            for row in xrange(firstCol, rowNb, 2):
                for col in xrange(colNb):
                    setCellColour(row, col, colour)

        setCellColour(0, rowNb, colNb, 'White')
        setCellColour(1, rowNb, colNb, colourWhiteSmoke)

    def CheckTransactionModification(self, askConfirmation=True):
        """ Return True if we can can pursue the flow. False else. 
            Force Save if askConfirmation is False.
        """
        if self.HasEntryBeenModified():
            toBeSaved = wx.ID_YES
            if askConfirmation:
                dlg = wx.MessageDialog(self, 'Do you want to save entry modifications?', 'Question', wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION | wx.STAY_ON_TOP)
                toBeSaved = dlg.ShowModal()
                dlg.Destroy()
            if toBeSaved == wx.ID_CANCEL:
                self.SelectRow(self.GetGridCursorRow())
                return False
            if toBeSaved == wx.ID_YES:
                self.PostTransaction()
            elif toBeSaved == wx.ID_NO:
                self.ReleaseEntryForModification()
                self.RefreshView(sort=False)
        return True

    def HasEntryBeenModified(self):
        return hasattr(self, '_entryProxy')

    def ReleaseEntryForModification(self):
        try:
            del self._entryProxy
        except:
            pass

    def GetModifiedEntry(self):
        return self._entryProxy

    def PrepareEntryForModification(self, entry):
        self._entryProxy = entry.getProxy()
        return self._entryProxy

    def PostTransaction(self):
        """ Return the Entry whose Transaction has been modified. """
        modified = self.GetModifiedEntry()
        original = modified.getOriginalObject()
        original.transaction.post(modified)
        self.ReleaseEntryForModification()
        return original