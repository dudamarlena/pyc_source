# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/debugger/breakpoints.py
# Compiled at: 2019-09-09 02:52:13
# Size of source mod 2**32: 11097 bytes
from noval import GetApp, _, NewId
import os, noval.constants as constants, noval.ui_base as ui_base, noval.iface as iface, noval.plugin as plugin
from tkinter import ttk
import noval.ttkwidgets.treeviewframe as treeviewframe, noval.imageutils as imageutils, noval.consts as consts, noval.menu as tkmenu, noval.util.utils as utils

class BreakpointExceptionDialog(ui_base.CommonModaldialog):
    EXCEPTIONS = [
     'ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError',
     'BytesWarning', 'DeprecationWarning', 'EOFError', 'EnvironmentError', 'Exception',
     'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError',
     'ImportWarning', 'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt',
     'LookupError', 'MemoryError', 'NameError', 'NotImplementedError', 'OSError', 'OverflowError',
     'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError',
     'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TypeError',
     'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
     'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError']

    def __init__(self, parent, dlg_id, title):
        self.filters = []
        wx.Dialog.__init__(self, parent, dlg_id, title)
        boxsizer = wx.BoxSizer(wx.VERTICAL)
        boxsizer.Add(wx.StaticText(self, -1, _('Break when exception is:'), style=wx.ALIGN_CENTRE), 0, flag=wx.ALL, border=SPACE)
        self.listbox = wx.CheckListBox(self, -1, size=(400, 300), choices=[])
        boxsizer.Add(self.listbox, 0, flag=wx.EXPAND | wx.BOTTOM | wx.RIGHT, border=SPACE)
        lineSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.select_all_btn = wx.Button(self, -1, _('Select All'))
        wx.EVT_BUTTON(self.select_all_btn, -1, self.SelectAll)
        lineSizer.Add(self.select_all_btn, 0, flag=wx.LEFT, border=SPACE)
        self.unselect_all_btn = wx.Button(self, -1, _('UnSelect All'))
        wx.EVT_BUTTON(self.unselect_all_btn, -1, self.UnSelectAll)
        lineSizer.Add(self.unselect_all_btn, 0, flag=wx.LEFT, border=SPACE)
        boxsizer.Add(lineSizer, 0, flag=wx.RIGHT | wx.ALIGN_RIGHT, border=SPACE)
        boxsizer.Add(wx.StaticText(self, -1, _('User defined exceptions:'), style=wx.ALIGN_CENTRE), 0, flag=wx.BOTTOM | wx.RIGHT | wx.TOP, border=SPACE)
        self.other_exception_ctrl = wx.TextCtrl(self, -1, '', size=(-1, -1))
        boxsizer.Add(self.other_exception_ctrl, 0, flag=wx.BOTTOM | wx.RIGHT | wx.EXPAND, border=SPACE)
        lineSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_exception_btn = wx.Button(self, -1, _('Add Exception'))
        wx.EVT_BUTTON(self.add_exception_btn, -1, self.AddException)
        lineSizer.Add(self.add_exception_btn, 0, flag=wx.LEFT, border=SPACE)
        boxsizer.Add(lineSizer, 0, flag=wx.RIGHT | wx.ALIGN_RIGHT | wx.BOTTOM, border=SPACE)
        bsizer = wx.StdDialogButtonSizer()
        ok_btn = wx.Button(self, wx.ID_OK, _('&OK'))
        wx.EVT_BUTTON(ok_btn, -1, self.OnOKClick)
        ok_btn.SetDefault()
        bsizer.AddButton(ok_btn)
        cancel_btn = wx.Button(self, wx.ID_CANCEL, _('&Cancel'))
        bsizer.AddButton(cancel_btn)
        bsizer.Realize()
        boxsizer.Add(bsizer, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM | wx.TOP, HALF_SPACE)
        self.SetSizer(boxsizer)
        self.Fit()
        self.InitExceptions()
        self.exceptions = []

    def OnOKClick(self, event):
        for i in range(self.listbox.GetCount()):
            if self.listbox.IsChecked(i):
                exception = self.listbox.GetString(i)
                self.exceptions.append(exception)

        self.EndModal(wx.ID_OK)

    def InitExceptions(self):
        descr = ''
        for exception in self.EXCEPTIONS:
            self.listbox.Append(exception)

    def SelectAll(self, event):
        for i in range(self.listbox.GetCount()):
            if not self.listbox.IsChecked(i):
                self.listbox.Check(i, True)

    def UnSelectAll(self, event):
        for i in range(self.listbox.GetCount()):
            if self.listbox.IsChecked(i):
                self.listbox.Check(i, False)

    def AddException(self, event):
        other_exception = self.other_exception_ctrl.GetValue().strip()
        if other_exception == '':
            return
        self.listbox.Append(other_exception)


class BreakpointsUI(treeviewframe.TreeViewFrame):
    FILE_NAME_COLUMN_WIDTH = 150
    FILE_LINE_COLUMN_WIDTH = 50
    clearBPID = NewId()
    syncLineID = NewId()

    def __init__(self, parent):
        columns = ['File', 'Line', 'Path']
        treeviewframe.TreeViewFrame.__init__(self, parent, columns=columns, show='headings', displaycolumns=(0,
                                                                                                             1,
                                                                                                             2))
        self.currentItem = None
        for column in columns:
            self.tree.heading(column, text=_(column))

        self.tree.column('0', width=100, anchor='w')
        self.tree.column('1', width=60, anchor='w')
        self.breakpoint_bmp = imageutils.load_image('', 'python/debugger/breakpoint.png')
        self.tree.bind('<3>', self.OnListRightClick, True)
        self.tree.bind('<Double-Button-1>', self.OnDoubleClick, '+')
        self.currentItem = None
        self._masterBPDict = {}
        self.PopulateBPList()

    def PopulateBPList(self):
        breakpoints = utils.profile_get('MasterBreakpointDict', [])
        for dct in breakpoints:
            self.tree.insert('', 'end', image=self.breakpoint_bmp, values=(dct['filename'], dct['lineno'], dct['path']))
            self.AddBreakpoint(dct['path'], dct['lineno'])

    def OnDoubleClick(self, event):
        if not self.tree.selection():
            return
        self.currentItem = self.tree.selection()[0]
        self.SyncBPLine()

    def OnListRightClick(self, event):
        if not self.tree.selection():
            return
        self.currentItem = self.tree.selection()[0]
        menu = tkmenu.PopupMenu()
        item = tkmenu.MenuItem(self.clearBPID, _('Clear Breakpoint'), None, None, None)
        menu.AppendMenuItem(item, handler=self.ClearBreakPoint)
        item = tkmenu.MenuItem(self.syncLineID, _('Goto Source Line'), None, None, None)
        menu.AppendMenuItem(item, handler=self.SyncBPLine)
        item = tkmenu.MenuItem(constants.ID_CLEAR_ALL_BREAKPOINTS, _('&Clear All Breakpoints'), None, None, None)
        menu.AppendMenuItem(item, handler=self.ClearAllBreakPoints)
        menu.tk_popup(event.x_root, event.y_root)

    def SyncBPLine(self):
        if self.currentItem != None:
            values = self.tree.item(self.currentItem, 'values')
            fileName = values[2]
            lineNumber = values[1]
            GetApp().GotoView(fileName, int(lineNumber))

    def ClearBreakPoint(self):
        if self.currentItem != None:
            self.DeleteBreakPoint(self.currentItem)

    def DeleteBreakPoint(self, item, notify=True):
        values = self.tree.item(item, 'values')
        fileName = values[2]
        lineNumber = values[1]
        doc = GetApp().GetDocumentManager().GetDocument(fileName)
        if doc:
            doc.GetFirstView().DeleteBpMark(int(lineNumber), notify=notify)
        else:
            self.tree.delete(item)
            self.RemoveBreakpoint(fileName, lineNumber, notify)

    def ListItemSelected(self, event):
        self.currentItem = event.m_itemIndex

    def ListItemDeselected(self, event):
        self.currentItem = -1

    def ToogleBreakpoint(self, lineno, filename, delete=False, notify=True):
        if not delete:
            self.tree.insert('', 'end', image=self.breakpoint_bmp, values=(os.path.basename(filename), lineno, filename))
            self.AddBreakpoint(filename, lineno)
            if GetApp().GetDebugger()._debugger_ui:
                GetApp().GetDebugger()._debugger_ui.NotifyDebuggersOfBreakpointChange()
        else:
            for child in self.tree.get_children():
                values = self.tree.item(child, 'values')
                if values[1] == lineno and values[2] == filename:
                    self.tree.delete(child)
                    self.RemoveBreakpoint(filename, lineno, notify)
                    break

    def ClearAllBreakPoints(self):
        for child in self.tree.get_children():
            self.DeleteBreakPoint(child, notify=False)

        if GetApp().GetDebugger()._debugger_ui is not None:
            GetApp().GetDebugger()._debugger_ui.NotifyDebuggersOfBreakpointChange()

    def SaveBreakpoints(self):
        breakpoints = []
        for child in self.tree.get_children():
            values = self.tree.item(child, 'values')
            dct = {'filename': values[0], 
             'lineno': values[1], 
             'path': values[2]}
            breakpoints.append(dct)

        utils.profile_set('MasterBreakpointDict', breakpoints)

    def GetMasterBreakpointDict(self):
        return self._masterBPDict

    def AddBreakpoint(self, filename, lineno):
        """
            通知断点服务器添加断点
        """
        lineno = int(lineno)
        if filename not in self._masterBPDict:
            self._masterBPDict[filename] = [
             lineno]
        else:
            self._masterBPDict[filename] += [lineno]

    def RemoveBreakpoint(self, filename, lineno, notify=True):
        """
            通知断点服务器删除断点
        """
        lineno = int(lineno)
        if filename not in self._masterBPDict:
            utils.get_logger().error('In ClearBreak: no filename %s', filename)
            return
        if lineno in self._masterBPDict[filename]:
            self._masterBPDict[filename].remove(lineno)
            if self._masterBPDict[filename] == []:
                del self._masterBPDict[filename]
            if notify and GetApp().GetDebugger()._debugger_ui:
                GetApp().GetDebugger()._debugger_ui.NotifyDebuggersOfBreakpointChange()
        else:
            utils.get_logger().error('In ClearBreak: no filename %s line %d', filename, lineno)


class BreakpointsViewLoader(plugin.Plugin):
    plugin.Implements(iface.CommonPluginI)

    def Load(self):
        GetApp().MainFrame.AddView(consts.BREAKPOINTS_TAB_NAME, BreakpointsUI, _('Break Points'), 'se', image_file='python/debugger/breakpoints.png')