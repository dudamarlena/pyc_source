# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/debugger/output.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1927 bytes
from noval import GetApp, _
from tkinter import messagebox
from noval.project.output import *

class DebugOutputctrl(CommonOutputctrl):

    def __init__(self, parent, is_debug=False, **kwargs):
        CommonOutputctrl.__init__(self, parent, **kwargs)
        self._is_debug = is_debug

    def OnDoubleClick(self, event):
        line, col = self.GetCurrentLineColumn()
        lineText = self.GetLineText(line)
        fileBegin = lineText.find('File "')
        fileEnd = lineText.find('", line ')
        lineEnd = lineText.find(', in ')
        if lineText == '\n' or fileBegin == -1 or fileEnd == -1:
            lineNumber = self.GetCurrentLine()
            if lineNumber == 0:
                return
            lineText = self.GetLineText(lineNumber - 1)
            fileBegin = lineText.find('File "')
            fileEnd = lineText.find('", line ')
            lineEnd = lineText.find(', in ')
            if lineText == '\n' or fileBegin == -1 or fileEnd == -1:
                pass
            return
        filename = lineText[fileBegin + 6:fileEnd]
        if filename == '<string>':
            return
        if -1 == lineEnd:
            lineNum = int(lineText[fileEnd + 8:])
        else:
            lineNum = int(lineText[fileEnd + 8:lineEnd])
        if filename and not os.path.exists(filename):
            messagebox.showerror(_('File Error'), _("The file '%s' doesn't exist and couldn't be opened!") % filename, parent=self.master)
            return
        GetApp().GotoView(filename, lineNum, load_outline=False)
        self.ActivateView()


class DebugOutputView(CommononOutputview):

    def __init__(self, master, is_debug=False):
        CommononOutputview.__init__(self, master)

    def GetOuputctrlClass(self):
        return DebugOutputctrl