# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_fmgr.py
# Compiled at: 2012-06-09 14:19:29
"""

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id:  $'
__revision__ = '$Revision:  $'
import wx, wx.aui as aui
EVT_AUI_PANE_CLOSE = aui.EVT_AUI_PANE_CLOSE
EVT_AUI_PANE_RESTORE = aui.EVT_AUI_PANE_RESTORE

class EdFrameManager(aui.AuiManager):
    """Frame manager for external components to abstract underlying manager"""

    def __init__(self, wnd=None, flags=0):
        """Create the frame manager object
        @param wnd: Frame to manage
        @param flags: frame manager flags

        """
        super(EdFrameManager, self).__init__(wnd, flags)
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        self.Bind(aui.EVT_AUI_PANE_RESTORE, self.OnPaneRestore)

    def OnPaneClose(self, evt):
        """Notify pane it is being closed"""
        evt.Skip()

    def OnPaneRestore(self, evt):
        """Notify pane it is being opened"""
        evt.Skip()

    def AddPane(self, wnd, info=None, caption=None):
        return super(EdFrameManager, self).AddPane(wnd, info, caption)

    def IsEditorMaximized(self):
        """Is the editor pane maximized?
        return: bool

        """
        bEditMax = True
        for pane in self.GetAllPanes():
            if pane.IsShown() and pane.name != 'EditPane':
                bEditMax = False
                break

        return bEditMax


EdPaneInfo = aui.AuiPaneInfo