# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/find/findresult.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 4320 bytes
from noval import GetApp, _
import os, tkinter as tk
from tkinter import messagebox
import noval.iface as iface, noval.plugin as plugin, noval.consts as consts
from tkinter import ttk
import noval.editor.text as texteditor
from noval.find.findindir import FILENAME_MARKER, PROJECT_MARKER, FILE_MARKER, FindIndirService
import noval.ttkwidgets.textframe as textframe, noval.ui_base as ui_base, noval.util.utils as utils

class FindResultsview(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        text_frame = textframe.TextFrame(self, borderwidth=0, text_class=texteditor.TextCtrl, font='SmallEditorFont', read_only=True, undo=False)
        self.text = text_frame.text
        text_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.text.bind('<Double-Button-1>', self.OnJumptoFoundLine, '+')
        self._ui_theme_change_binding = self.bind('<<ThemeChanged>>', self.reload_ui_theme, True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def destroy(self):
        self.unbind('<<ThemeChanged>>')
        ttk.Frame.destroy(self)

    def reload_ui_theme(self, event=None):
        self.text._reload_theme_options(force=True)

    def AddLine(self, line_text):
        self.text.set_read_only(False)
        if utils.is_linux():
            line_text = line_text.strip()
        self.text.insert(tk.END, line_text)
        if not line_text.endswith('\n'):
            self.text.insert(tk.END, '\n')
        self.text.set_read_only(True)

    def ClearLines(self):
        self.text.set_read_only(False)
        self.text.delete('1.0', 'end')
        self.text.set_read_only(True)

    def OnJumptoFoundLine(self, event=None, defLineNum=-1):
        if 0 == self.text.GetCurrentLine():
            return
        if defLineNum == -1:
            defLineNum = self.text.GetCurrentLine()
        lineText = self.text.GetLineText(defLineNum)
        if lineText == '\n' or lineText.find(FILENAME_MARKER) != -1 or lineText.find(PROJECT_MARKER) != -1 or lineText.find(FILE_MARKER) != -1 or defLineNum == 1:
            return
        lineEnd = lineText.find(':')
        if lineEnd == -1:
            return
        lineNum = int(lineText[0:lineEnd].replace(FindIndirService.LINE_PREFIX, '').strip())
        filename = self.GetDefineFilename(defLineNum)
        foundDoc = GetApp().GetDocumentManager().GetDocument(filename)
        foundView = None
        if not foundDoc:
            if not os.path.exists(filename):
                messagebox.showerror(_('Open File Error'), _("The file '%s' doesn't exist and couldn't be opened!") % filename)
                return
        GetApp().GotoView(filename, lineNum, load_outline=False)

    def GetTextLineEndPosition(self, linenum):
        pos = 0
        for iline in range(linenum):
            col = self.text.index('%d.end' % (iline + 1)).split('.')[1]
            pos += int(col)

        return pos

    def GetDefineFilename(self, defLineNum):
        while defLineNum > 0:
            lineText = self.text.GetLineText(defLineNum)
            if lineText.find(FILENAME_MARKER) != -1 and lineText.find(FindIndirService.LINE_PREFIX) == -1:
                filename = lineText.replace(FILENAME_MARKER, '').strip()
                return filename
            defLineNum -= 1

    def ScrolltoEnd(self):
        self.text.ScrolltoEnd()


class FindResultsviewLoader(plugin.Plugin):
    plugin.Implements(iface.CommonPluginI)

    def Load(self):
        GetApp().MainFrame.AddView(consts.SEARCH_RESULTS_VIEW_NAME, FindResultsview, _('Search Results'), 's', image_file='search.ico', default_position_key=2)