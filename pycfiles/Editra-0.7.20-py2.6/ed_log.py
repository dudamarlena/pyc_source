# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_log.py
# Compiled at: 2012-07-28 13:46:45
"""
Editra LogViewer

This module provides classes for managing the log display and filtering of its
messages. The module also exports an implementation of a shelf plugin for
displaying a L{LogViewer} in the Shelf.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_log.py 72223 2012-07-28 17:35:57Z CJP $'
__revision__ = '$Revision: 72223 $'
import os, re, wx, ed_msg, eclib, iface, plugin
from profiler import Profile_Get
import ed_glob, ed_basewin
_ = wx.GetTranslation
SHOW_ALL_MSG = 'ALL'

class EdLogViewer(plugin.Plugin):
    """Shelf interface implementation for the log viewer"""
    plugin.Implements(iface.ShelfI)
    __name__ = 'Editra Log'

    @staticmethod
    def AllowMultiple():
        """EdLogger allows multiple instances"""
        return True

    @staticmethod
    def CreateItem(parent):
        """Returns a log viewr panel"""
        return LogViewer(parent)

    def GetBitmap(self):
        """Get the log viewers tab icon
        @return: wx.Bitmap

        """
        bmp = wx.ArtProvider.GetBitmap(str(self.GetId()), wx.ART_MENU)
        return bmp

    @staticmethod
    def GetId():
        """Plugin menu identifier ID"""
        return ed_glob.ID_LOGGER

    @staticmethod
    def GetMenuEntry(menu):
        """Get the menu entry for the log viewer
        @param menu: the menu items parent menu

        """
        return wx.MenuItem(menu, ed_glob.ID_LOGGER, _('Editra Log'), _("View Editra's console log"))

    def GetName(self):
        """Return the name of this control"""
        return self.__name__

    @staticmethod
    def IsStockable():
        """EdLogViewer can be saved in the shelf preference stack"""
        return True


class LogViewer(ed_basewin.EdBaseCtrlBox):
    """LogViewer is a control for displaying and working with output
    from Editra's log.

    """

    def __init__(self, parent):
        super(LogViewer, self).__init__(parent)
        self._buffer = LogBuffer(self)
        self.SetWindow(self._buffer)
        self._srcfilter = None
        self._clear = None
        self.__DoLayout()
        self.Bind(wx.EVT_BUTTON, lambda evt: self._buffer.Clear(), self._clear)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self._srcfilter)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        ed_msg.Subscribe(self.OnThemeChange, ed_msg.EDMSG_THEME_CHANGED)
        return

    def OnDestroy(self, evt):
        """Cleanup and unsubscribe from messages"""
        if evt.GetId() == self.GetId():
            ed_msg.Unsubscribe(self.OnThemeChange)

    def __DoLayout(self):
        """Layout the log viewer window"""
        ctrlbar = self.CreateControlBar(wx.TOP)
        self._srcfilter = wx.Choice(ctrlbar, wx.ID_ANY, choices=[])
        ctrlbar.AddControl(wx.StaticText(ctrlbar, label=_('Show output from') + ':'))
        ctrlbar.AddControl(self._srcfilter)
        ctrlbar.AddStretchSpacer()
        self._clear = self.AddPlateButton(_('Clear'), ed_glob.ID_DELETE, wx.ALIGN_RIGHT)

    def OnChoice(self, evt):
        """Set the filter based on the choice controls value
        @param evt: wx.CommandEvent

        """
        self._buffer.SetFilter(self._srcfilter.GetStringSelection())

    def OnThemeChange(self, msg):
        """Update the buttons icon when the icon theme changes
        @param msg: Message Object

        """
        cbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_DELETE), wx.ART_MENU)
        self._clear.SetBitmap(cbmp)
        self._clear.Refresh()

    def SetSources(self, srclist):
        """Set the list of available log sources in the choice control
        @param srclist: list of log sources

        """
        choice = self._srcfilter.GetStringSelection()
        lst = sorted(srclist)
        lst.insert(0, _('All'))
        self._srcfilter.SetItems(lst)
        if not self._srcfilter.SetStringSelection(choice):
            self._srcfilter.SetSelection(0)


class LogBuffer(eclib.OutputBuffer):
    """Buffer for displaying log messages that are sent on Editra's
    log channel.
    @todo: make line buffering configurable through interface

    """
    RE_WARN_MSG = re.compile('\\[err\\]|\\[error\\]|\\[warn\\]')
    ERROR_STYLE = eclib.OPB_STYLE_MAX + 1

    def __init__(self, parent):
        super(LogBuffer, self).__init__(parent)
        self._filter = SHOW_ALL_MSG
        self._srcs = list()
        self.SetLineBuffering(2000)
        font = Profile_Get('FONT1', 'font', wx.Font(11, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.SetFont(font)
        style = (font.GetFaceName(), font.GetPointSize(), '#FF0000')
        self.StyleSetSpec(LogBuffer.ERROR_STYLE, 'face:%s,size:%d,fore:#FFFFFF,back:%s' % style)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy, self)
        ed_msg.Subscribe(self.UpdateLog, ed_msg.EDMSG_LOG_ALL)

    def OnDestroy(self, evt):
        """Unregister from receiving any more log messages"""
        if evt.GetId() == self.GetId():
            ed_msg.Unsubscribe(self.UpdateLog)
        evt.Skip()

    def AddFilter(self, src):
        """Add a new filter source
        @param src: filter source string
        @postcondition: if src is new the parent window is updated

        """
        if src not in self._srcs:
            self._srcs.append(src)
            self.Parent.SetSources(self._srcs)

    def ApplyStyles(self, start, txt):
        """Apply coloring to error and warning messages
        @note: overridden from L{outbuff.OutputBuffer}
        @param start: Start position of text that needs styling in the buffer
        @param txt: The string of text that starts at the start position in the
                    buffer.

        """
        for group in LogBuffer.RE_WARN_MSG.finditer(txt):
            sty_s = start + group.start()
            sty_e = start + group.end()
            self.StartStyling(sty_s, 255)
            self.SetStyling(sty_e - sty_s, LogBuffer.ERROR_STYLE)

    def SetFilter(self, src):
        """Set the level of what is shown in the display
        @param src: Only show messages from src
        @return: bool

        """
        if src in self._srcs:
            self._filter = src
            return True
        else:
            if src == _('All'):
                self._filter = SHOW_ALL_MSG
                return True
            return False

    def UpdateLog(self, msg):
        """Add a new log message
        @param msg: Message Object containing a LogMsg

        """
        if wx.Thread_IsMain():
            self.DoUpdateLog(msg)
        else:
            wx.CallAfter(self.DoUpdateLog, msg)

    def DoUpdateLog(self, msg):
        if not self.IsRunning():
            self.Start(200)
        logmsg = msg.GetData()
        org = logmsg.Origin
        if org not in self._srcs:
            self.AddFilter(org)
        if self._filter == SHOW_ALL_MSG:
            self.AppendUpdate(unicode(logmsg) + unicode(os.linesep))
        elif self._filter == logmsg.Origin:
            msg = '[%s][%s]%s' % (logmsg.ClockTime, logmsg.Type, logmsg.Value)
            self.AppendUpdate(msg + unicode(os.linesep))