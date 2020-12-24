# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/debugger/debugger.py
# Compiled at: 2019-10-07 21:21:23
# Size of source mod 2**32: 14205 bytes
from noval import NewId, GetApp, _
import tkinter as tk
from tkinter import ttk, messagebox
import sys
from noval.project.debugger import *
import traceback, noval.python.debugger.watchs as watchs, pickle
from noval.python.debugger.commandui import BaseDebuggerUI, ShowBreakdebugViews, RunCommandUI
import noval.menu as tkmenu
from noval.python.debugger.executor import PythonExecutor

class PythonDebugger(Debugger):
    RUN_PARAMETERS = []
    _debugger_ui = None

    def __init__(self):
        Debugger.__init__(self)
        self._exceptions = []
        self._frame = None
        self.projectPath = None
        self.phpDbgParam = None
        self._tabs_menu = None
        self._popup_index = -1
        self._watch_separater = None

    @classmethod
    def SetDebuggerUI(cls, debugger_ui):
        cls._debugger_ui = debugger_ui

    def GetExceptions(self):
        return self._exceptions

    def SetExceptions(self, exceptions):
        self._exceptions = exceptions

    def _right_btn_press(self, event):
        try:
            index = self.bottomTab.index('@%d,%d' % (event.x, event.y))
            self._popup_index = index
            self.create_tab_menu()
        except Exception:
            utils.get_logger().exception('Opening tab menu')

    def GetBottomtabInstancePage(self, index):
        tab_page = self.bottomTab.get_child_by_index(index)
        page = tab_page.winfo_children()[0]
        return page

    def CloseAllPages(self):
        """
            关闭并移除所有运行调式标签页
        """
        close_suc = True
        for i in range(self.bottomTab.GetPageCount() - 1, -1, -1):
            page = self.GetBottomtabInstancePage(i)
            close_suc = self.ClosePage(page)
            if not close_suc:
                return False

        return close_suc

    def ClosePage(self, page=None):
        """
            关闭并移除单个运行调式标签页
        """
        if page is None:
            page = self.GetBottomtabInstancePage(self._popup_index)
        if hasattr(page, 'StopAndRemoveUI'):
            return page.StopAndRemoveUI()
        return True

    def create_tab_menu(self):
        """
        Handles right clicks for the notebook, enabling users to either close
        a tab or select from the available documents if the user clicks on the
        notebook's white space.
        """
        if self._popup_index < 0:
            return
        page = self.GetBottomtabInstancePage(self._popup_index)
        if not hasattr(page, 'StopAndRemoveUI'):
            return
        if self._tabs_menu is None:
            menu = tkmenu.PopupMenu(self.bottomTab.winfo_toplevel())
            self._tabs_menu = menu
            menu.Append(constants.ID_CLOSE, _('Close'), handler=self.ClosePage)
            menu.Append(constants.ID_CLOSE_ALL, _('Close All'), handler=self.CloseAllPages)
        self._tabs_menu.tk_popup(*self.bottomTab.winfo_toplevel().winfo_pointerxy())

    def CheckScript(self):
        if not PythonExecutor.GetPythonExecutablePath():
            return
        interpreter = GetApp().GetCurrentInterpreter()
        doc_view = self.GetActiveView()
        if not doc_view:
            return
        document = doc_view.GetDocument()
        if not document.Save() or document.IsNewDocument:
            return
        if not os.path.exists(interpreter.Path):
            wx.MessageBox("Could not find '%s' on the path." % interpreter.Path, _('Interpreter not exists'), wx.OK | wx.ICON_ERROR, wx.GetApp().GetTopWindow())
            return
        ok, line, msg = interpreter.CheckSyntax(document.GetFilename())
        if ok:
            messagebox.showinfo(GetApp().GetAppName(), _('Check Syntax Ok!'), parent=doc_view.GetFrame())
            return
        messagebox.showerror(GetApp().GetAppName(), msg, parent=doc_view.GetFrame())
        if line > 0:
            doc_view.GotoLine(line)

    def Runfile(self, filetoRun=None):
        self.GetCurrentProject().Run(filetoRun)

    @common_run_exception
    def RunWithoutDebug(self, filetoRun=None):
        self.GetCurrentProject().RunWithoutDebug(filetoRun)

    @common_run_exception
    def RunLast(self):
        self.GetCurrentProject().RunLast()

    @common_run_exception
    def DebugLast(self):
        self.GetCurrentProject().DebugRunLast()

    @common_run_exception
    def RunLast(self):
        self.GetCurrentProject().RunLast()

    def StepNext(self):
        if BaseDebuggerUI.DebuggerRunning():
            self._debugger_ui.OnNext()
        else:
            self.GetCurrentProject().BreakintoDebugger()

    def StepInto(self):
        if BaseDebuggerUI.DebuggerRunning():
            self._debugger_ui.OnSingleStep()
        else:
            self.GetCurrentProject().BreakintoDebugger()

    def SetParameterAndEnvironment(self):
        self.GetCurrentProject().SetParameterAndEnvironment()

    @classmethod
    def CloseDebugger(cls):
        try:
            if cls._debugger_ui is not None:
                cls._debugger_ui.framesTab.watchsTab.SaveWatchs()
                cls._debugger_ui.framesTab.breakPointsTab.SaveBreakpoints()
            if not RunCommandUI.StopAndRemoveAllUI():
                return False
        except:
            tp, val, tb = sys.exc_info()
            traceback.print_exception(tp, val, tb)

        return True

    def AppendRunParameter(self, run_paramteter):
        if len(self.RUN_PARAMETERS) > 0:
            self.GetCurrentProject().SaveRunParameter(self.RUN_PARAMETERS[(-1)])
        self.RUN_PARAMETERS.append(run_paramteter)

    def IsFileContainBreakPoints(self, document):
        """
            判断单个文件是否包含断点信息
        """
        doc_path = document.GetFilename()
        masterBPDict = GetApp().MainFrame.GetView(consts.BREAKPOINTS_TAB_NAME).GetMasterBreakpointDict()
        if doc_path in masterBPDict and len(masterBPDict[doc_path]) > 0:
            return True
        return False

    def CreateDebuggerMenuItem(self, runMenu, menu_id, text, image, handler, menu_index):
        """
            添加断点调式菜单项,如果菜单项已经存在不能重复添加
        """
        if not runMenu.FindMenuItem(menu_id):
            runMenu.Insert(menu_index, menu_id, text, img=image, handler=handler)

    def DeleteDebuggerMenuItem(self, runMenu, menu_id):
        """
            删除断点调式菜单项,只有在菜单项已经存在时才能删除
        """
        if runMenu.FindMenuItem(menu_id):
            menu_index = runMenu.GetMenuIndex(menu_id)
            runMenu.delete(menu_index, menu_index)

    def ShowHideDebuggerMenu(self, show=True):
        run_menu = GetApp().Menubar.GetRunMenu()
        if show:
            menu_index = 3
            self.CreateDebuggerMenuItem(run_menu, constants.ID_RESTART_DEBUGGER, _('&Restart'), self._debugger_ui.restart_bmp, self._debugger_ui.RestartDebugger, menu_index)
            self.CreateDebuggerMenuItem(run_menu, constants.ID_TERMINATE_DEBUGGER, _('&Stop Debugging'), self._debugger_ui.stop_bmp, self._debugger_ui.StopExecution, menu_index)
            self.CreateDebuggerMenuItem(run_menu, constants.ID_BREAK_INTO_DEBUGGER, _('&Break'), self._debugger_ui.break_bmp, self._debugger_ui.BreakExecution, menu_index)
            self.CreateDebuggerMenuItem(run_menu, constants.ID_STEP_CONTINUE, _('&Continue'), self._debugger_ui.continue_bmp, self._debugger_ui.OnContinue, menu_index)
            self.CreateDebuggerMenuItem(run_menu, constants.ID_STEP_OUT, _('&Step Out'), self._debugger_ui.stepOut_bmp, self._debugger_ui.OnStepOut, 11)
            self.CreateDebuggerMenuItem(run_menu, constants.ID_QUICK_ADD_WATCH, _('&Quick add Watch'), self._debugger_ui.quick_watch_bmp, self._debugger_ui.OnQuickAddWatch, 12)
            self.CreateDebuggerMenuItem(run_menu, constants.ID_ADD_WATCH, _('&Add Watch'), self._debugger_ui.watch_bmp, self._debugger_ui.OnAddWatch, 13)
            ShowBreakdebugViews(True)
        else:
            self.DeleteDebuggerMenuItem(run_menu, constants.ID_STEP_OUT)
            self.DeleteDebuggerMenuItem(run_menu, constants.ID_TERMINATE_DEBUGGER)
            self.DeleteDebuggerMenuItem(run_menu, constants.ID_STEP_CONTINUE)
            self.DeleteDebuggerMenuItem(run_menu, constants.ID_BREAK_INTO_DEBUGGER)
            self.DeleteDebuggerMenuItem(run_menu, constants.ID_RESTART_DEBUGGER)
            self.DeleteDebuggerMenuItem(run_menu, constants.ID_ADD_WATCH)
            self.DeleteDebuggerMenuItem(run_menu, constants.ID_QUICK_ADD_WATCH)
            ShowBreakdebugViews(False)

    def AddtoWatchText(self, text):
        self._debugger_ui.framesTab.AddtoWatchExpression(text, text)

    def AddWatchText(self, text, quick_watch=False):
        self._debugger_ui.framesTab.AddWatchExpression(text, text, quick_watch)


class DebuggerOptionsPanel(ttk.Frame):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        SPACE = 10
        config = wx.ConfigBase_Get()
        localHostStaticText = wx.StaticText(self, -1, _('Local Host Name:'))
        self._LocalHostTextCtrl = wx.TextCtrl(self, -1, config.Read('DebuggerHostName', DEFAULT_HOST), size=(150,
                                                                                                             -1))
        portNumberStaticText = wx.StaticText(self, -1, _('Port Range:'))
        dashStaticText = wx.StaticText(self, -1, _('through to'))
        startingPort = config.ReadInt('DebuggerStartingPort', DEFAULT_PORT)
        self._PortNumberTextCtrl = wx.lib.intctrl.IntCtrl(self, -1, startingPort, size=(50,
                                                                                        -1))
        self._PortNumberTextCtrl.SetMin(1)
        self._PortNumberTextCtrl.SetMax(65514)
        self.Bind(wx.lib.intctrl.EVT_INT, self.MinPortChange, self._PortNumberTextCtrl)
        self._EndPortNumberTextCtrl = wx.lib.intctrl.IntCtrl(self, -1, startingPort + PORT_COUNT, size=(50,
                                                                                                        -1))
        self._EndPortNumberTextCtrl.SetMin(22)
        self._EndPortNumberTextCtrl.SetMax(65535)
        self._EndPortNumberTextCtrl.Enable(False)
        debuggerPanelBorderSizer = wx.BoxSizer(wx.VERTICAL)
        debuggerPanelSizer = wx.GridBagSizer(hgap=5, vgap=5)
        debuggerPanelSizer.Add(localHostStaticText, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        debuggerPanelSizer.Add(self._LocalHostTextCtrl, (0, 1), (1, 3), flag=wx.EXPAND | wx.ALIGN_CENTER)
        debuggerPanelSizer.Add(portNumberStaticText, (1, 0), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        debuggerPanelSizer.Add(self._PortNumberTextCtrl, (1, 1), flag=wx.ALIGN_CENTER)
        debuggerPanelSizer.Add(dashStaticText, (1, 2), flag=wx.ALIGN_CENTER)
        debuggerPanelSizer.Add(self._EndPortNumberTextCtrl, (1, 3), flag=wx.ALIGN_CENTER)
        FLUSH_PORTS_ID = wx.NewId()
        self._flushPortsButton = wx.Button(self, FLUSH_PORTS_ID, 'Reset Port List')
        wx.EVT_BUTTON(parent, FLUSH_PORTS_ID, self.FlushPorts)
        debuggerPanelSizer.Add(self._flushPortsButton, (2, 2), (1, 2), flag=wx.ALIGN_RIGHT)
        debuggerPanelBorderSizer.Add(debuggerPanelSizer, 0, wx.ALL, SPACE)
        self.SetSizer(debuggerPanelBorderSizer)
        self.Layout()

    def FlushPorts(self, event):
        if self._PortNumberTextCtrl.IsInBounds():
            config = wx.ConfigBase_Get()
            config.WriteInt('DebuggerStartingPort', self._PortNumberTextCtrl.GetValue())
            PythonDebuggerUI.NewPortRange()
        else:
            wx.MessageBox(_('The starting port is not valid. Please change the value and try again.'), _('Invalid Starting Port Number'))

    def MinPortChange(self, event):
        self._EndPortNumberTextCtrl.Enable(True)
        self._EndPortNumberTextCtrl.SetValue(self._PortNumberTextCtrl.GetValue() + PORT_COUNT)
        self._EndPortNumberTextCtrl.Enable(False)

    def OnOK(self, optionsDialog):
        config = wx.ConfigBase_Get()
        config.Write('DebuggerHostName', self._LocalHostTextCtrl.GetValue())
        if self._PortNumberTextCtrl.IsInBounds():
            config.WriteInt('DebuggerStartingPort', self._PortNumberTextCtrl.GetValue())
        return True

    def GetIcon(self):
        return getContinueIcon()