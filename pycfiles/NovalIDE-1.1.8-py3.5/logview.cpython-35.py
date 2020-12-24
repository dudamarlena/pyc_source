# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/logview.py
# Compiled at: 2019-10-07 21:21:23
# Size of source mod 2**32: 8014 bytes
from noval import GetApp, _, NewId
import os, sys, logging, tkinter as tk
from tkinter import ttk
import noval.editor.text as texteditor, noval.util.utils as utils, noval.toolbar as toolbar, noval.ttkwidgets.textframe as textframe

class LogCtrl(texteditor.TextCtrl):

    def __init__(self, parent, **kwargs):
        texteditor.TextCtrl.__init__(self, parent, **kwargs)

    def SetViewDefaults(self):
        """ Needed to override default """
        pass

    def ClearAll(self):
        self.delete('1.0', 'end')


class LogView(ttk.Frame):
    ID_SETTINGS = NewId()
    ID_CLEAR = NewId()

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.textCtrl = None
        self._loggers = []
        self._CreateControl()

    def _CreateControl(self):
        self._tb = toolbar.ToolBar(self, orient=tk.HORIZONTAL)
        self._tb.pack(fill='x', expand=0)
        self._tb.AddLabel(text=_('Logger Name:'))
        self.logCtrl = self._tb.AddCombox()
        self.logCtrl['values'] = self._loggers
        self.logmameVar = tk.StringVar()
        self.logCtrl['textvariable'] = self.logmameVar
        self.logCtrl.bind('<<ComboboxSelected>>', self.OnLogChoice)
        self._tb.AddLabel(text=_('Logger Level:'))
        log_levels = [
         '', logging.getLevelName(logging.INFO),
         logging.getLevelName(logging.WARN), logging.getLevelName(logging.ERROR), logging.getLevelName(logging.CRITICAL)]
        self.loglevelCtrl = self._tb.AddCombox()
        self.loglevelVar = tk.StringVar()
        self.loglevelCtrl['textvariable'] = self.loglevelVar
        self.loglevelCtrl['values'] = log_levels
        self.loglevelCtrl.bind('<<ComboboxSelected>>', self.OnLogLevelChoice)
        self._tb.AddButton(self.ID_CLEAR, None, 'Clear', handler=self.ClearLines, style=None)
        text_frame = textframe.TextFrame(self, text_class=LogCtrl, undo=False)
        self.textCtrl = text_frame.text
        self.log_ctrl_handler = LogCtrlHandler(self)
        self.log_ctrl_handler.setLevel(logging.INFO)
        self.textCtrl.set_read_only(True)
        text_frame.pack(fill='both', expand=1)
        logging.getLogger().addHandler(self.log_ctrl_handler)

    def OnSettingsClick(self):
        import LoggingConfigurationService
        dlg = LoggingConfigurationService.LoggingOptionsDialog(wx.GetApp().GetTopWindow())
        dlg.ShowModal()

    def OnDoubleClick(self, event):
        lineText, pos = self.textCtrl.GetCurLine()
        fileBegin = lineText.find('File "')
        fileEnd = lineText.find('", line ')
        lineEnd = lineText.find(', in ')
        if lineText == '\n' or fileBegin == -1 or fileEnd == -1 or lineEnd == -1:
            lineNumber = self.textCtrl.GetCurrentLine()
            if lineNumber == 0:
                return
            lineText = self.textCtrl.GetLine(lineNumber - 1)
            fileBegin = lineText.find('File "')
            fileEnd = lineText.find('", line ')
            lineEnd = lineText.find(', in ')
            if lineText == '\n' or fileBegin == -1 or fileEnd == -1 or lineEnd == -1:
                pass
            return
        filename = lineText[fileBegin + 6:fileEnd]
        lineNum = int(lineText[fileEnd + 8:lineEnd])
        foundView = None
        openDocs = wx.GetApp().GetDocumentManager().GetDocuments()
        for openDoc in openDocs:
            if openDoc.GetFilename() == filename:
                foundView = openDoc.GetFirstView()
                break

        if not foundView:
            doc = wx.GetApp().GetDocumentManager().CreateDocument(filename, wx.lib.docview.DOC_SILENT | wx.lib.docview.DOC_OPEN_ONCE)
            foundView = doc.GetFirstView()
        if foundView:
            foundView.Activate()
            foundView.GetFrame().SetFocus()
            foundView.GotoLine(lineNum)
            startPos = foundView.PositionFromLine(lineNum)
            lineText = foundView.GetCtrl().GetLine(lineNum - 1)
            foundView.SetSelection(startPos, startPos + len(lineText.rstrip('\n')))
            import OutlineService
            wx.GetApp().GetService(OutlineService.OutlineService).LoadOutline(foundView, position=startPos)

    def OnLogChoice(self, event):
        logname = self.logmameVar.get()
        if logname == '':
            self.log_ctrl_handler.ClearFilters()
        else:
            filter = logging.Filter(logname)
            self.log_ctrl_handler.addFilter(filter)

    def OnLogLevelChoice(self, event):
        log_level_name = self.loglevelVar.get()
        if log_level_name == '':
            self.log_ctrl_handler.setLevel(logging.NOTSET)
        else:
            log_level = logging._checkLevel(log_level_name)
            self.log_ctrl_handler.setLevel(log_level)

    def ClearLines(self):
        self.textCtrl.set_read_only(False)
        self.textCtrl.ClearAll()
        self.textCtrl.set_read_only(True)

    def AddLine(self, text, log_level):
        self.textCtrl.set_read_only(False)
        if utils.is_linux():
            line_text = text.strip()
        self.textCtrl.insert(tk.END, text)
        if not text.endswith('\n'):
            self.textCtrl.insert(tk.END, '\n')
        self.textCtrl.set_read_only(True)

    def AddLogger(self, name):
        if name not in self._loggers:
            self._loggers.append(name)
        self.logCtrl['values'] = self._loggers


class LogCtrlHandler(logging.Handler):

    def __init__(self, log_view):
        logging.Handler.__init__(self)
        self._log_view = log_view
        self.setLevel(logging.DEBUG)
        self.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s'))

    def emit(self, record):
        level = record.levelno
        msg = self.format(record)
        self._log_view.AddLogger(record.name)
        self._log_view.AddLine(msg + os.linesep, level)

    def ClearFilters(self):
        self.filters = []

    def addFilter(self, filter):
        self.ClearFilters()
        logging.Handler.addFilter(self, filter)