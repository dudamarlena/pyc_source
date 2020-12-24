# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_statbar.py
# Compiled at: 2012-03-17 12:57:55
"""
Custom StatusBar for Editra that contains a progress bar that responds to
messages from ed_msg to display progress of different actions.

@summary: Editra's StatusBar class

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_statbar.py 70229 2012-01-01 01:27:10Z CJP $'
__revision__ = '$Revision: 70229 $'
import wx, wx.stc, ed_glob, util, ed_msg, ed_menu
from syntax.synglob import GetDescriptionFromId
from eclib import ProgressStatusBar, EncodingDialog
from extern.decorlib import anythread
_ = wx.GetTranslation

class EdStatBar(ProgressStatusBar):
    """Custom status bar that handles dynamic field width adjustment and
    automatic expiration of status messages.

    """
    ID_CLEANUP_TIMER = wx.NewId()

    def __init__(self, parent):
        super(EdStatBar, self).__init__(parent, style=wx.ST_SIZEGRIP)
        self._pid = parent.GetId()
        self._widths = list()
        self._cleanup_timer = wx.Timer(self, EdStatBar.ID_CLEANUP_TIMER)
        self._eolmenu = wx.Menu()
        self._lexmenu = None
        self._log = wx.GetApp().GetLog()
        self.SetFieldsCount(6)
        self.SetStatusWidths([-1, 90, 40, 40, 40, 155])
        self._eolmenu.Append(ed_glob.ID_EOL_MAC, 'CR', _('Change line endings to %s') % 'CR', kind=wx.ITEM_CHECK)
        self._eolmenu.Append(ed_glob.ID_EOL_WIN, 'CRLF', _('Change line endings to %s') % 'CRLF', kind=wx.ITEM_CHECK)
        self._eolmenu.Append(ed_glob.ID_EOL_UNIX, 'LF', _('Change line endings to %s') % 'LF', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy, self)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_TIMER, self.OnExpireMessage, id=EdStatBar.ID_CLEANUP_TIMER)
        ed_msg.Subscribe(self.OnProgress, ed_msg.EDMSG_PROGRESS_SHOW)
        ed_msg.Subscribe(self.OnProgress, ed_msg.EDMSG_PROGRESS_STATE)
        ed_msg.Subscribe(self.OnUpdateText, ed_msg.EDMSG_UI_SB_TXT)
        ed_msg.Subscribe(self.OnUpdateDoc, ed_msg.EDMSG_UI_NB_CHANGED)
        ed_msg.Subscribe(self.OnUpdateDoc, ed_msg.EDMSG_FILE_SAVED)
        ed_msg.Subscribe(self.OnUpdateDoc, ed_msg.EDMSG_FILE_OPENED)
        ed_msg.Subscribe(self.OnUpdateDoc, ed_msg.EDMSG_UI_STC_LEXER)
        return

    def OnDestroy(self, evt):
        """Unsubscribe from messages"""
        if self._lexmenu:
            self._lexmenu.Destroy()
        if self._eolmenu:
            self._eolmenu.Destroy()
        if evt.GetId() == self.GetId():
            ed_msg.Unsubscribe(self.OnProgress)
            ed_msg.Unsubscribe(self.OnUpdateText)
            ed_msg.Unsubscribe(self.OnUpdateDoc)
        evt.Skip()

    def __SetStatusText(self, txt, field):
        """Safe method to use for setting status text with CallAfter.
        @param txt: string
        @param field: int

        """
        try:
            super(EdStatBar, self).SetStatusText(txt, field)
            self.AdjustFieldWidths()
            if field == ed_glob.SB_INFO and txt != '':
                if self._cleanup_timer.IsRunning():
                    self._cleanup_timer.Stop()
                self._cleanup_timer.Start(10000, True)
        except wx.PyDeadObjectError, wx.PyAssertionError:
            pass
        except TypeError, err:
            self._log('[edstatbar][err] Bad status message: %s' % str(txt))
            self._log('[edstatbar][err] %s' % err)

    def AdjustFieldWidths(self):
        """Adjust each field width of status bar basing on the field text
        @return: None

        """
        widths = [
         -1]
        for field in [ed_glob.SB_BUFF,
         ed_glob.SB_LEXER,
         ed_glob.SB_ENCODING,
         ed_glob.SB_EOL,
         ed_glob.SB_ROWCOL]:
            width = self.GetTextExtent(self.GetStatusText(field))[0] + 20
            if width == 20:
                width = 0
            widths.append(width)

        if widths[(-1)] < 155:
            widths[-1] = 155
        if widths != self._widths:
            self._widths = widths
            self.SetStatusWidths(self._widths)

    def GetMainWindow(self):
        """Method required for L{ed_msg.mwcontext}"""
        return self.TopLevelParent

    def OnExpireMessage(self, evt):
        """Handle Expiring the status message when the oneshot timer
        tells us it has expired.

        """
        if evt.GetId() == EdStatBar.ID_CLEANUP_TIMER:
            wx.CallAfter(self.__SetStatusText, '', ed_glob.SB_INFO)
        else:
            evt.Skip()

    def OnLeftDClick(self, evt):
        """Handlers mouse left double click on status bar
        @param evt: wx.MouseEvent
        @note: Assumes parent is MainWindow instance

        """
        pt = evt.GetPosition()
        if self.GetFieldRect(ed_glob.SB_ROWCOL).Contains(pt):
            mw = self.GetParent()
            mpane = mw.GetEditPane()
            mpane.ShowCommandControl(ed_glob.ID_GOTO_LINE)
        else:
            evt.Skip()

    def OnLeftUp(self, evt):
        """Handle left clicks on the status bar
        @param evt: wx.MouseEvent

        """
        pt = evt.GetPosition()
        if self.GetFieldRect(ed_glob.SB_EOL).Contains(pt):
            rect = self.GetFieldRect(ed_glob.SB_EOL)
            self.PopupMenu(self._eolmenu, (rect.x, rect.y))
        elif self.GetFieldRect(ed_glob.SB_ENCODING).Contains(pt):
            nb = self.GetTopLevelParent().GetNotebook()
            buff = nb.GetCurrentCtrl()
            dlg = EncodingDialog(nb, msg=_('Change the encoding of the current document.'), title=_('Change Encoding'), default=buff.GetEncoding())
            bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_DOCPROP), wx.ART_OTHER)
            if bmp.IsOk():
                dlg.SetBitmap(bmp)
            dlg.CenterOnParent()
            if dlg.ShowModal() == wx.ID_OK:
                buff.SetEncoding(dlg.GetEncoding())
                self.UpdateFields()
            if dlg:
                dlg.Destroy()
        elif self.GetFieldRect(ed_glob.SB_LEXER).Contains(pt):
            if self._lexmenu:
                self._lexmenu.Destroy()
            self._lexmenu = wx.Menu()
            ed_menu.EdMenuBar.PopulateLexerMenu(self._lexmenu)
            rect = self.GetFieldRect(ed_glob.SB_LEXER)
            self.PopupMenu(self._lexmenu, (rect.x, rect.y))
        else:
            evt.Skip()

    def OnProgress(self, msg):
        """Set the progress bar's state
        @param msg: Message Object

        """
        mdata = msg.GetData()
        if self._pid != mdata[0]:
            return
        mtype = msg.GetType()
        if mtype == ed_msg.EDMSG_PROGRESS_STATE:
            self.SetProgress(mdata[1])
            self.range = mdata[2]
            if sum(mdata[1:]) == 0:
                self.Stop()
        elif mtype == ed_msg.EDMSG_PROGRESS_SHOW:
            if mdata[1]:
                self.Start(75)
            else:
                self.Stop()

    @ed_msg.mwcontext
    def OnUpdateDoc(self, msg):
        """Update document related fields
        @param msg: Message Object

        """
        self.UpdateFields()
        if msg.GetType() == ed_msg.EDMSG_UI_NB_CHANGED:
            wx.CallAfter(self.__SetStatusText, '', ed_glob.SB_INFO)

    @anythread
    def DoUpdateText(self, msg):
        """Thread safe update of status text. Proxy for OnUpdateText because
        pubsub seems to have issues with passing decorator methods for
        listeners.
        @param msg: Message Object

        """
        parent = self.GetTopLevelParent()
        if parent.IsActive() or wx.GetApp().GetTopWindow() == parent:
            (field, txt) = msg.GetData()
            self.UpdateFields()
            wx.CallAfter(self.__SetStatusText, txt, field)

    def OnUpdateText(self, msg):
        """Update the status bar text based on the received message
        @param msg: Message Object

        """
        self.DoUpdateText(msg)

    def PushStatusText(self, txt, field):
        """Set the status text
        @param txt: Text to put in bar
        @param field: int

        """
        wx.CallAfter(self.__SetStatusText, txt, field)

    def SetStatusText(self, txt, field):
        """Set the status text
        @param txt: Text to put in bar
        @param field: int

        """
        wx.CallAfter(self.__SetStatusText, txt, field)

    def UpdateFields(self):
        """Update document fields based on the currently selected
        document in the editor.
        @postcondition: encoding and lexer fields are updated
        @todo: update when readonly hooks are implemented

        """
        nb = self.GetParent().GetNotebook()
        if nb is None:
            return
        else:
            try:
                cbuff = nb.GetCurrentCtrl()
                doc = cbuff.GetDocument()
                wx.CallAfter(self.__SetStatusText, doc.GetEncoding(), ed_glob.SB_ENCODING)
                wx.CallAfter(self.__SetStatusText, GetDescriptionFromId(cbuff.GetLangId()), ed_glob.SB_LEXER)
                eol = {wx.stc.STC_EOL_CR: 'CR', wx.stc.STC_EOL_LF: 'LF', 
                   wx.stc.STC_EOL_CRLF: 'CRLF'}
                wx.CallAfter(self.__SetStatusText, eol[cbuff.GetEOLMode()], ed_glob.SB_EOL)
            except wx.PyDeadObjectError:
                return

            return