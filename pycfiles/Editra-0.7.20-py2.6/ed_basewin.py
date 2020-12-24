# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_basewin.py
# Compiled at: 2012-06-09 14:19:30
"""
This module provides base classes for windows and dialogs to be used within
Editra.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_basewin.py 71697 2012-06-08 15:20:22Z CJP $'
__revision__ = '$Revision: 71697 $'
import wx, ed_msg, eclib, util

def FindMainWindow(window):
    """Find the MainWindow of the given window
        @return: MainWindow or None

        """

    def IsMainWin(win):
        """Check if the given window is a main window"""
        return getattr(win, '__name__', '') == 'MainWindow'

    if IsMainWin(window):
        return window
    else:
        tlw = window.GetTopLevelParent()
        if IsMainWin(tlw):
            return tlw
        if hasattr(tlw, 'GetParent'):
            tlw = tlw.GetParent()
            if IsMainWin(tlw):
                return tlw
        return


class EDBaseFileTree(eclib.FileTree):
    """Base file view control. Contains some common functionality
    that should not be included in the low level control.

    """

    def __init__(self, parent):
        super(EDBaseFileTree, self).__init__(parent)
        ed_msg.Subscribe(self.OnActivateMsg, ed_msg.EDMSG_UI_MW_ACTIVATE)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)

    def OnDestroy(self, event):
        """Cleanup message handlers"""
        if self:
            ed_msg.Unsubscribe(self.OnActivateMsg)
            self.DoOnDestroy()
        event.Skip()

    def OnActivateMsg(self, msg):
        """Handle activation messages"""
        mw = FindMainWindow(self)
        if mw and msg.Context == mw.Id:
            self.DoOnActivate(msg.Data['active'])

    def DoOnActivate(self, active):
        """Handle activation event
        @param active: bool - window active or inactive

        """
        pass

    def DoOnDestroy(self):
        """Handle window destruction"""
        pass


class EdBaseDialog(eclib.ECBaseDlg):
    """Editra Dialog Base Class"""

    def __init__(self, parent, id=wx.ID_ANY, title='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE, name='EdBaseDialog'):
        super(EdBaseDialog, self).__init__(parent, id, title, pos, size, style, name)


class EdBaseFrame(wx.Frame):
    """Editra Frame Base Class"""

    def __init__(self, parent, id=wx.ID_ANY, title='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name='EdBaseFrame'):
        super(EdBaseFrame, self).__init__(parent, id, title, pos, size, style, name)
        util.SetWindowIcon(self)
        wx.GetApp().RegisterWindow(repr(self), self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        """Handle frame closure event"""
        wx.GetApp().UnRegisterWindow(repr(self))
        event.Skip()


class EdBaseCtrlBox(eclib.ControlBox):
    """ControlBox base class to be used by all common components"""

    def __init__(self, parent):
        super(EdBaseCtrlBox, self).__init__(parent)
        ed_msg.Subscribe(self._OnFontChange, ed_msg.EDMSG_DSP_FONT)
        self.Bind(wx.EVT_WINDOW_DESTROY, self._OnDestroy)

    def _OnDestroy(self, evt):
        if self and evt.GetEventObject is self:
            ed_msg.Unsubscribe(self._OnFontChange)

    def _OnFontChange(self, msg):
        """Update font of all controls"""
        if not self:
            return
        font = msg.GetData()
        if isinstance(font, wx.Font):
            for pos in (wx.TOP, wx.BOTTOM, wx.LEFT, wx.RIGHT):
                cbar = self.GetControlBar(pos)
                if cbar:
                    for child in cbar.GetChildren():
                        child.SetFont(font)

    def AddPlateButton(self, lbl='', bmp=-1, align=wx.ALIGN_LEFT, cbarpos=wx.TOP):
        """Add an eclib.PlateButton to the ControlBar specified by
        cbarpos.
        @keyword lbl: Button Label
        @keyword bmp: Bitmap or EditraArtProvider ID
        @keyword align: button alignment
        @keyword cbarpos: ControlBar position
        @return: PlateButton instance

        """
        ctrlbar = self.GetControlBar(cbarpos)
        assert ctrlbar is not None, 'No ControlBar at cbarpos'
        return ctrlbar.AddPlateButton(lbl, bmp, align)

    def CreateControlBar(self, pos=wx.TOP):
        """Override for CreateControlBar to automatically set the
        flat non-gradient version of the control under GTK.

        """
        cbar = super(EdBaseCtrlBox, self).CreateControlBar(pos)
        cbar.__class__ = EdBaseCtrlBar
        if wx.Platform == '__WXGTK__':
            cbar.SetWindowStyle(eclib.CTRLBAR_STYLE_DEFAULT | eclib.CTRLBAR_STYLE_BORDER_TOP | eclib.CTRLBAR_STYLE_BORDER_BOTTOM)
        cbar.SetMargins(2, 2)
        return cbar


class EdBaseCtrlBar(eclib.ControlBar):

    def AddPlateButton(self, lbl='', bmp=-1, align=wx.ALIGN_LEFT):
        """Add an eclib.PlateButton 
        @keyword lbl: Button Label
        @keyword bmp: Bitmap or EditraArtProvider ID
        @keyword align: button alignment
        @return: PlateButton instance

        """
        if not isinstance(bmp, wx.Bitmap):
            assert isinstance(bmp, int)
            bmp = wx.ArtProvider.GetBitmap(str(bmp), wx.ART_MENU)
        if bmp.IsNull() or not bmp.IsOk():
            bmp = None
        btn = eclib.PlateButton(self, wx.ID_ANY, lbl, bmp, style=eclib.PB_STYLE_NOBG)
        self.AddControl(btn, align)
        return btn