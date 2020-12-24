# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mathbench/lab/labbench.py
# Compiled at: 2008-04-05 13:51:29
"""
Inspired by
PyAlaCarte and PyAlaMode editors from WxPython

Combines the shell and filling into one control.
"""
import wx
from wx.py.shell import Shell
from mathbench.lab.logbook import LogBook
from mathbench.lab.apparatus import ApparatusTree

class LabBench(wx.SplitterWindow):
    """LabBench based on SplitterWindow."""
    sashoffset = 300

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.SP_3D | wx.SP_LIVE_UPDATE, name='LabBench Window', rootObject=None, rootLabel=None, rootIsNamespace=True, intro='', locals=None, InterpClass=None, startupScript=None, execStartupScript=True, *args, **kwds):
        """Create LabBench instance."""
        wx.SplitterWindow.__init__(self, parent, id, pos, size, style, name)
        self.shell = Shell(parent=self, introText=intro, locals=locals, InterpClass=InterpClass, startupScript=startupScript, execStartupScript=execStartupScript, *args, **kwds)
        self.editor = self.shell
        if rootObject is None:
            rootObject = self.shell.interp.locals
        self.apparatus = ApparatusTree(parent=self, rootObject=rootObject, rootLabel=rootLabel, rootIsNamespace=rootIsNamespace)
        self.SizeWindows()
        self.SplitVertically(self.apparatus, self.shell, self.sashoffset)
        self.SetMinimumPaneSize(200)
        self.Bind(wx.EVT_SIZE, self.SplitterOnSize)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnChanged)
        return

    def OnChanged(self, event):
        """update sash offset from the bottom of the window"""
        self.sashoffset = self.GetSize().height - event.GetSashPosition()
        event.Skip()

    def SplitterOnSize(self, event):
        splitter = event.GetEventObject()
        sz = splitter.GetSize()
        event.Skip()

    def saveHistory(self):
        """
                Save the command history in a file.
                """
        pass