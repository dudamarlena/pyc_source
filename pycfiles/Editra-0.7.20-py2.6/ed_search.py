# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_search.py
# Compiled at: 2012-06-09 14:19:30
"""@package Editra.src.ed_search

Provides text searching services, utilities, and ui components for searching
text documents and files.

@summary: Text searching and results presentation ui

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_search.py 71673 2012-06-06 20:12:42Z CJP $'
__revision__ = '$Revision: 71673 $'
import os, sys, re, unicodedata, wx, ed_glob, ed_txt, ed_msg, plugin, iface
from profiler import Profile_Get, Profile_Set
import eclib, ebmlib, ed_basewin, ed_thread
_ = wx.GetTranslation

class EdSearchEngine(ebmlib.SearchEngine):
    """Text searching engine"""

    def __init__(self, query, regex=True, down=True, matchcase=True, wholeword=False):
        super(EdSearchEngine, self).__init__(query, regex, down, matchcase, wholeword)
        self._offset = 0

    def FormatResult(self, fname, lnum, match):
        """Format the search result string for find all action that is performed
        on a selection.
        @return: string
        @todo: better unicode handling

        """
        fname = ed_txt.DecodeString(fname, sys.getfilesystemencoding())
        if not ebmlib.IsUnicode(fname):
            fname = _('DECODING ERROR')
        match = ed_txt.DecodeString(match)
        if not ebmlib.IsUnicode(match):
            match = _('DECODING ERROR')
        else:
            match = ' ' + match.lstrip()
        rstring = '%(fname)s (%(lnum)d): %(match)s'
        lnum = lnum + self._offset + 1
        return rstring % dict(fname=fname, lnum=lnum, match=match)

    def SetOffset(self, offset):
        """Set the offset for a search in selection action
        @param offset: int

        """
        self._offset = offset

    def SetQuery(self, query):
        """Set the query string"""
        if not ebmlib.IsUnicode(query):
            query = query.decode('utf-8')
        query = unicodedata.normalize('NFC', query)
        super(EdSearchEngine, self).SetQuery(query)

    def SetSearchPool(self, pool):
        """Set the search pool"""
        if not ebmlib.IsUnicode(pool):
            pool = pool.decode('utf-8')
        pool = unicodedata.normalize('NFC', pool)
        super(EdSearchEngine, self).SetSearchPool(pool)


class SearchController(object):
    """Controls the interface to the text search engine"""

    def __init__(self, owner, getstc):
        """Create the controller
        @param owner: View that owns this controller
        @param getstc: Callable to get the current buffer with

        """
        super(SearchController, self).__init__()
        self._parent = owner
        self._stc = getstc
        self._finddlg = None
        self._posinfo = dict(scroll=0, start=0, found=-1, ldir=None)
        self._data = self._InitFindData()
        self._li_choices = list()
        self._li_sel = 0
        self._filters = None
        self._clients = list()
        self._engine = EdSearchEngine('')
        self._engine.SetResultFormatter(self._engine.FormatResult)
        self._parent.Bind(eclib.EVT_FIND, self.OnFind)
        self._parent.Bind(eclib.EVT_FIND_NEXT, self.OnFind)
        self._parent.Bind(eclib.EVT_FIND_ALL, self.OnFindAll)
        self._parent.Bind(eclib.EVT_COUNT, self.OnCount)
        self._parent.Bind(eclib.EVT_REPLACE, self.OnReplace)
        self._parent.Bind(eclib.EVT_REPLACE_ALL, self.OnReplaceAll)
        self._parent.Bind(eclib.EVT_FIND_CLOSE, self.OnFindClose)
        self._parent.Bind(eclib.EVT_OPTION_CHANGED, self.OnOptionChanged)
        ed_msg.Subscribe(self._OnShowFindMsg, ed_msg.EDMSG_FIND_SHOW_DLG)
        return

    def __del__(self):
        """Cleanup message handlers"""
        ed_msg.Unsubscribe(self._OnShowFindMsg)
        if self._finddlg:
            self._finddlg.Destroy()

    def _CreateNewDialog(self, e_id):
        """Create and set the controllers find dialog
        @param e_id: Dialog Type Id

        """
        if not isinstance(self._parent, wx.Window):
            parent = wx.GetApp().GetActiveWindow()
            self._parent = parent
        else:
            parent = self._parent
        labels = (_('Find'), _('Find/Replace'))
        if e_id == ed_glob.ID_FIND_REPLACE:
            dlg = eclib.AdvFindReplaceDlg(parent, self._data, labels, eclib.AFR_STYLE_REPLACEDIALOG)
        elif e_id == ed_glob.ID_FIND:
            dlg = eclib.AdvFindReplaceDlg(parent, self._data, labels)
        else:
            dlg = None
        if dlg is not None:
            find = wx.ArtProvider.GetBitmap(str(ed_glob.ID_FIND), wx.ART_MENU)
            replace = wx.ArtProvider.GetBitmap(str(ed_glob.ID_FIND_REPLACE), wx.ART_MENU)
            if find is not None and find.IsOk():
                dlg.SetFindBitmap(find)
            if replace is not None and replace.IsOk():
                dlg.SetReplaceBitmap(replace)

            def GetCurrentDir():
                """Get current directory for dialog context
                @return: unicode

                """
                fname = ''
                if self:
                    cbuff = self._stc()
                    fname = getattr(cbuff, 'GetFileName', lambda : '')()
                return os.path.dirname(fname)

            dlg.SetDirectoryGetter(GetCurrentDir)
            dlg.SetLookinChoices(self._li_choices)
            dlg.SetLookinSelection(self._li_sel)
            dlg.SetFileFilters(self._filters)
        return dlg

    def _OnShowFindMsg(self, msg):
        """Message handler for clients to request and setup the find dialog
        with.
        @param msg: dict(mainw, lookin, findtxt)

        """
        data = msg.GetData()
        if data.get('mainw', None) == self._parent.TopLevelParent:
            if 'findtxt' in data:
                self.SetQueryString(data.get('findtxt'))
            else:
                query = self.GetClientString()
                if len(query):
                    self.SetQueryString(query)
            if self._finddlg is None:
                self._finddlg = self._CreateNewDialog(ed_glob.ID_FIND)
                if self._finddlg is None:
                    return
                self._finddlg.CenterOnParent()
                self._finddlg.SetTransparent(240)
            else:
                self._UpdateDialogState(ed_glob.ID_FIND)
            if 'lookin' in data:
                self._finddlg.SetLookinPath(data.get('lookin'))
            self._finddlg.Show()
            self._finddlg.Raise()
            self._finddlg.SetFocus()
        else:
            return
        return

    def _UpdateDialogState(self, e_id):
        """Update the state of the existing dialog"""
        if self._finddlg is None:
            self._finddlg = self._CreateNewDialog(e_id)
            self._finddlg.CenterOnParent()
        else:
            mode = self._finddlg.GetDialogMode()
            if e_id == ed_glob.ID_FIND and mode != eclib.AFR_STYLE_FINDDIALOG:
                self._finddlg.SetDialogMode(eclib.AFR_STYLE_FINDDIALOG)
            elif e_id == ed_glob.ID_FIND_REPLACE and mode != eclib.AFR_STYLE_REPLACEDIALOG:
                self._finddlg.SetDialogMode(eclib.AFR_STYLE_REPLACEDIALOG)
        self._finddlg.RefreshFindReplaceFields()
        self._finddlg.SetFocus()
        return

    def _InitFindData(self):
        """Get the intial find data
        @return: wx.FindReplaceData

        """
        fdata = Profile_Get('SEARCH_SETTINGS', default=None)
        if fdata is not None:
            fmap = dict(matchcase=eclib.AFR_MATCHCASE, wholeword=eclib.AFR_WHOLEWORD, regex=eclib.AFR_REGEX, recurse=eclib.AFR_RECURSIVE)
            flags = 0
            for flag in fdata:
                if fdata.get(flag, False):
                    flags |= fmap.get(flag, 0)

            fdata = wx.FindReplaceData(flags)
        else:
            fdata = wx.FindReplaceData(eclib.AFR_RECURSIVE)
        return fdata

    def _StoreFindData(self):
        """Serialize the find/replace settings into the user profile"""
        fmap = dict(matchcase=eclib.AFR_MATCHCASE, wholeword=eclib.AFR_WHOLEWORD, regex=eclib.AFR_REGEX, recurse=eclib.AFR_RECURSIVE)
        tostore = dict()
        flags = self._data.GetFlags()
        for fname in fmap:
            flag = fmap[fname]
            tostore[fname] = False
            if flags & flag:
                tostore[fname] = True

        Profile_Set('SEARCH_SETTINGS', tostore)

    def GetClientString(self, multiline=False):
        """Get the selected text in the current client buffer. By default
        it will only return the selected text if its on a single line.
        @keyword multiline: Return text if it is multiple lines
        @return: string

        """
        cbuff = self._stc()
        if cbuff is None:
            return ''
        else:
            (start, end) = cbuff.GetSelection()
            rtext = cbuff.GetSelectedText()
            if start != end:
                sline = cbuff.LineFromPosition(start)
                eline = cbuff.LineFromPosition(end)
                if not multiline and sline != eline:
                    rtext = ''
            return rtext

    def GetData(self):
        """Get the controllers FindReplaceData
        @return: wx.FindReplaceData

        """
        return self._data

    def GetDialog(self):
        """Return the active find dialog if one exists else return None
        @return: FindDialog or None

        """
        return self._finddlg

    def GetLastFound(self):
        """Returns the position value of the last found search item
        if the last search resulted in nothing being found then the
        return value will -1.
        @return: position of last search operation

        """
        return self._posinfo['found']

    def OnUpdateFindUI(self, evt):
        """Update ui handler for find related controls
        @param evt: updateui event

        """
        if evt.GetId() in (ed_glob.ID_FIND_PREVIOUS, ed_glob.ID_FIND_NEXT):
            evt.Enable(len(self.GetData().GetFindString()))
        else:
            evt.Skip()

    def OnCount(self, evt):
        """Count the number of matches"""
        stc = self._stc()
        query = evt.GetFindString()
        mode = evt.GetSearchType()
        engine = ebmlib.SearchEngine(query, evt.IsRegEx(), True, evt.IsMatchCase(), evt.IsWholeWord())
        if mode == eclib.LOCATION_CURRENT_DOC:
            engine.SetSearchPool(stc.GetText())
        elif mode == eclib.LOCATION_IN_SELECTION:
            engine.SetSearchPool(stc.GetSelectedText())
        else:
            return
        matches = engine.FindAll()
        if matches:
            count = len(matches)
        else:
            count = 0
        rmap = dict(term=query, count=count)
        wx.MessageBox(_("The search term '%(term)s' was found %(count)d times.") % rmap, _('Find Count'), wx.ICON_INFORMATION | wx.OK)

    def OnFind(self, evt, findnext=False, incremental=False):
        """Do an incremental search in the currently buffer
        @param evt: EVT_FIND, EVT_FIND_NEXT
        @keyword findnext: force a find next action
        @keyword incremental: perform an incremental search

        """
        data = self.GetData()
        if findnext or evt.GetEventType() == wx.wxEVT_COMMAND_MENU_SELECTED:
            flags = data.GetFlags()
            if not findnext and evt.GetId() == ed_glob.ID_FIND_PREVIOUS:
                flags |= eclib.AFR_UP
            elif eclib.AFR_UP & flags:
                flags ^= eclib.AFR_UP
            evt = eclib.FindEvent(eclib.edEVT_FIND_NEXT, flags=flags)
            evt.SetFindString(data.GetFindString())
        stc = self._stc()
        data.SetFindString(evt.GetFindString())
        isdown = not evt.IsUp()
        self._engine.SetQuery(data.GetFindString())
        self._engine.SetFlags(isregex=evt.IsRegEx(), matchcase=evt.IsMatchCase(), wholeword=evt.IsWholeWord(), down=isdown)
        if self._engine.GetQueryObject() is None:
            fail = ed_txt.DecodeString(self._engine.GetQuery(), 'utf-8')
            wx.MessageBox(_('Invalid expression "%s"') % fail, _('Regex Compile Error'), style=wx.OK | wx.CENTER | wx.ICON_ERROR)
            return
        else:
            self._engine.SetSearchPool(stc.GetText())
            if evt.GetEventType() == eclib.edEVT_FIND:
                if not incremental:
                    spos = stc.CurrentPos
                else:
                    spos = self._posinfo['found']
                    if spos < 0:
                        spos = stc.CurrentPos
            else:
                spos = stc.CurrentPos
                (start, end) = stc.GetSelection()
                if start != end:
                    if isdown:
                        spos = max(start, end)
                    else:
                        spos = min(start, end)
            match = self._engine.Find(spos)
            if match is not None:
                (start, end) = match
                if isdown:
                    start = start + spos
                    end = end + spos
                    stc.SetSelection(start, end)
                else:
                    stc.SetSelection(start, end)
                stc.EnsureCaretVisible()
                line = stc.LineFromPosition(start)
                stc.EnsureVisible(line)
                self._posinfo['found'] = start
                ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT, (
                 ed_glob.SB_INFO, ''))
            else:
                if isdown:
                    match = self._engine.Find(0)
                    ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT, (
                     ed_glob.SB_INFO, _('Search wrapped to top')))
                else:
                    match = self._engine.Find(-1)
                    ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT, (
                     ed_glob.SB_INFO,
                     _('Search wrapped to bottom')))
                if match is not None:
                    (start, end) = match
                    self._posinfo['found'] = start
                    stc.SetSelection(start, end)
                    stc.EnsureCaretVisible()
                    line = stc.LineFromPosition(start)
                    stc.EnsureVisible(line)
                else:
                    self._posinfo['found'] = -1
                    fail = ed_txt.DecodeString(self._engine.GetQuery(), 'utf-8')
                    ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT, (
                     ed_glob.SB_INFO,
                     _('"%s" was not found') % fail))
            return

    def OnFindAll(self, evt):
        """Find all results for the given query and display results in a
        L{SearchResultScreen} in the Shelf.

        """
        smode = evt.GetSearchType()
        query = evt.GetFindString()
        if not query:
            return
        engine = EdSearchEngine(query, evt.IsRegEx(), True, evt.IsMatchCase(), evt.IsWholeWord())
        engine.SetResultFormatter(engine.FormatResult)
        if smode == eclib.LOCATION_CURRENT_DOC:
            stc = self._stc()
            fname = stc.GetFileName()
            if len(fname):
                ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH, (
                 engine.SearchInFile, [fname], dict()))
            else:
                engine.SetSearchPool(stc.GetText())
                ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH, (
                 engine.FindAllLines,))
        if smode == eclib.LOCATION_IN_SELECTION:
            stc = self._stc()
            sel_s = min(stc.GetSelection())
            offset = stc.LineFromPosition(sel_s)
            engine.SetOffset(offset)
            engine.SetSearchPool(stc.GetSelectedText())
            ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH, (
             engine.FindAllLines,))
        elif smode == eclib.LOCATION_OPEN_DOCS:
            files = [ fname.GetFileName() for fname in self._parent.GetTextControls() ]
            ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH, (
             engine.SearchInFiles, [files], dict()))
        elif smode == eclib.LOCATION_IN_CURRENT_DIR:
            stc = self._stc()
            path = ebmlib.GetPathName(stc.GetFileName())
            engine.SetFileFilters(evt.GetFileFilters())
            ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH, (
             engine.SearchInDirectory,
             [
              path], dict(recursive=evt.IsRecursive())))
        elif smode == eclib.LOCATION_IN_FILES:
            path = evt.GetDirectory()
            engine.SetFileFilters(evt.GetFileFilters())
            ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH, (
             engine.SearchInDirectory,
             [
              path], dict(recursive=evt.IsRecursive())))

    def OnFindSelected(self, evt):
        """Set the search query to the selected text and progress the search
        to the next match.

        """
        stc = self._stc()
        fstring = stc.GetSelectedText()
        if fstring:
            data = self.GetData()
            data.SetFindString(fstring)
            self.OnFind(evt)
        else:
            evt.Skip()

    def OnFindClose(self, evt):
        """Process storing search dialog state when it is closed
        @param evt: findlg.EVT_FIND_CLOSE

        """
        if self._finddlg is not None:
            self._li_choices = self._finddlg.GetLookinChoices()
            self._li_sel = self._finddlg.GetLookinSelection()
            self._filters = self._finddlg.GetFileFilters()
            if len(self._li_choices) > 8:
                choices = self._li_choices[-8:]
            else:
                choices = self._li_choices
            Profile_Set('SEARCH_LOC', choices)
            Profile_Set('SEARCH_FILTER', self._filters)
            self._StoreFindData()
            self._finddlg.Destroy()
            self._finddlg = None
        buff = wx.GetApp().GetCurrentBuffer()
        if buff:
            buff.SetFocus()
        return

    def OnOptionChanged(self, evt):
        """Handle when the find options are changed in the dialog"""
        self._StoreFindData()
        dead = list()
        for (idx, client) in enumerate(self._clients):
            try:
                client.NotifyOptionChanged(evt)
            except wx.PyDeadObjectError:
                dead.append(idx)

    def OnReplace(self, evt):
        """Replace the selected text in the current buffer
        @param evt: finddlg.EVT_REPLACE

        """
        replacestring = evt.GetReplaceString()
        if evt.IsRegEx() and self._engine is not None:
            match = self._engine.GetLastMatch()
            if match is not None:
                try:
                    value = match.expand(replacestring)
                except re.error, err:
                    msg = _('Error in regular expression expansion.The replace action cannot be completed.\n\nError Message: %s') % err.message
                    wx.MessageBox(msg, _('Replace Error'), wx.OK | wx.ICON_ERROR)
                    return

            else:
                value = replacestring
        else:
            value = replacestring
        sel = self._stc().GetSelection()
        if sel[0] == sel[1]:
            return
        else:
            self._stc().ReplaceSelection(value)
            eid = ed_glob.ID_FIND_NEXT
            if evt.IsUp():
                eid = ed_glob.ID_FIND_PREVIOUS
            tevt = eclib.FindEvent(eclib.edEVT_FIND_NEXT, eid)
            tevt.SetFlags(evt.GetFlags())
            tevt.SetFindString(evt.GetFindString())
            self.OnFind(tevt)
            return

    def OnReplaceAll(self, evt):
        """Replace all instance of the search string with the given
        replace string for the given search context.

        """
        smode = evt.GetSearchType()
        rstring = evt.GetReplaceString()
        engine = EdSearchEngine(evt.GetFindString(), evt.IsRegEx(), True, evt.IsMatchCase(), evt.IsWholeWord())
        engine.SetResultFormatter(engine.FormatResult)
        results = 0
        if smode == eclib.LOCATION_CURRENT_DOC:
            stc = self._stc()
            engine.SetSearchPool(stc.GetText())
            matches = engine.FindAll()
            if matches is not None:
                self.ReplaceInStc(stc, matches, rstring, evt.IsRegEx())
                results = len(matches)
        else:
            if smode == eclib.LOCATION_IN_SELECTION:
                stc = self._stc()
                engine.SetSearchPool(stc.GetSelectedText())
                matches = engine.FindAll()
                if matches is not None:
                    self.ReplaceInStcSelection(stc, matches, rstring, evt.IsRegEx())
                    results = len(matches)
            elif smode == eclib.LOCATION_OPEN_DOCS:
                for ctrl in self._parent.GetTextControls():
                    engine.SetSearchPool(ctrl.GetText())
                    matches = engine.FindAll()
                    if matches is not None:
                        self.ReplaceInStc(ctrl, matches, rstring, evt.IsRegEx())
                        results += len(matches)

            elif smode in (eclib.LOCATION_IN_CURRENT_DIR, eclib.LOCATION_IN_FILES):
                dlg = wx.MessageDialog(self._parent, _('Sorry will be ready for future version'), _('Not implemented'), style=wx.ICON_WARNING | wx.OK | wx.CANCEL | wx.CENTER)
                result = dlg.ShowModal()
                dlg.Destroy()
                if result == wx.ID_OK:
                    pass
                else:
                    return
            if results > 0:
                ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT, (
                 ed_glob.SB_INFO,
                 _('%d matches were replaced.') % results))
            return

    def OnShowFindDlg(self, evt):
        """Catches the Find events and shows the appropriate find dialog
        @param evt: event that called this handler
        @postcondition: find dialog is shown

        """
        query = self.GetClientString()
        if len(query):
            self.SetQueryString(query)
        eid = evt.GetId()
        if self._finddlg is None:
            self._finddlg = self._CreateNewDialog(eid)
            if self._finddlg is None:
                evt.Skip()
                return
            self._finddlg.CenterOnParent()
            self._finddlg.SetTransparent(240)
            self._finddlg.Show()
        else:
            self._UpdateDialogState(eid)
            self._finddlg.Show()
            self._finddlg.Raise()
        self._finddlg.SetFocus()
        return

    def RegisterClient(self, client):
        """Register a client object of this search controller. The client object
        must implement a method called NotifyOptionChanged to be called when
        search options are changed.

        >>> def NotifyOptionChanged(self, evt)

        @param client: object

        """
        if client not in self._clients:
            self._clients.append(client)

    def RemoveClient(self, client):
        """Remove a client from this controller
        @param client: object

        """
        if client in self._clients:
            self._clients.remove(client)

    @staticmethod
    def ReplaceInStc(stc, matches, rstring, isregex=True):
        """Replace the strings at the position in the given StyledTextCtrl
        @param stc: StyledTextCtrl
        @param matches: list of match objects
        @param rstring: Replace string
        @keyword isregex: Is it a regular expression operation (bool)

        """
        if not len(matches):
            return

        def GetSub(match):
            """replace substitution callable for re.sub"""
            value = rstring
            if isregex:
                try:
                    value = match.expand(rstring)
                except:
                    pass

            return value

        text = re.sub(matches[0].re, GetSub, stc.GetText())
        with eclib.Freezer(stc) as (_tmp):
            stc.BeginUndoAction()
            cpos = stc.CurrentPos
            stc.ClearAll()
            stc.SetText(text)
            stc.GotoPos(cpos)
            stc.EndUndoAction()

    @staticmethod
    def ReplaceInStcSelection(stc, matches, rstring, isregex=True):
        """Replace all the matches in the selection"""
        if not len(matches):
            return

        def GetSub(match):
            """replace substitution callable for re.sub"""
            value = rstring
            if isregex:
                try:
                    value = match.expand(rstring)
                except:
                    pass

            return value

        text = re.sub(matches[0].re, GetSub, stc.GetSelectedText())
        with eclib.Freezer(stc) as (_tmp):
            stc.BeginUndoAction()
            (start, end) = stc.GetSelection()
            stc.ReplaceSelection(text)
            stc.SetSelection(start, start + len(text))
            stc.EndUndoAction()

    def SetFileFilters(self, filters):
        """Set the file filter to use
        @param filters: string '*.py *.pyw'

        """
        self._filters = filters

    def SetLookinChoices(self, choices):
        """Set the list of locations to use for the recent search
        locations.
        @param choices: list of strings

        """
        self._li_choices = choices

    def SetQueryString(self, query):
        """Sets the search query value
        @param query: string to search for

        """
        self._data.SetFindString(query)

    def SetSearchFlags(self, flags):
        """Set the find services search flags
        @param flags: bitmask of parameters to set

        """
        self._data.SetFlags(flags)
        if self._finddlg is not None:
            self._finddlg.SetData(self._data)
        self._StoreFindData()
        return

    def RefreshControls(self):
        """Refresh controls that are associated with this controllers data."""
        if self._finddlg is not None:
            self._finddlg.RefreshFindOptions()
        self._StoreFindData()
        return


class EdSearchCtrl(wx.SearchCtrl):
    """Creates a simple search control for use in the toolbar
    or a statusbar and the such. Supports incremental search,
    and uses L{SearchController} to do the actual searching of the
    document.

    """

    def __init__(self, parent, id_, value='', menulen=0, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TE_RICH2 | wx.TE_PROCESS_ENTER):
        """Initializes the Search Control
        @param parent: parent window
        @param id_: control id
        @keyword value: default value
        @keyword menulen: max length of history menu
        @keyword pos: control position (tuple)
        @keyword size: control size (tuple)
        @keyword style: control style bitmask

        """
        super(EdSearchCtrl, self).__init__(parent, id_, value, pos, size, style)
        self._parent = parent
        self.FindService = self.GetTopLevelParent().GetNotebook()._searchctrl
        self._recent = list()
        self._last = None
        self.rmenu = wx.Menu()
        self.max_menu = menulen + 2
        self._txtctrl = None
        lbl = self.rmenu.Append(wx.ID_ANY, _('Recent Searches'))
        lbl.Enable(False)
        self.rmenu.AppendSeparator()
        self.SetMenu(self.rmenu)
        if wx.Platform in ('__WXMSW__', '__WXGTK__'):
            for child in self.GetChildren():
                if isinstance(child, wx.TextCtrl):
                    child.Bind(wx.EVT_KEY_UP, self.ProcessEvent)
                    child.Bind(wx.EVT_KEY_DOWN, self.ProcessEvent)
                    self._txtctrl = child
                    break

        else:
            self.Bind(wx.EVT_KEY_UP, self.ProcessEvent)
            self.Bind(wx.EVT_KEY_DOWN, self.ProcessEvent)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel)
        self.Bind(wx.EVT_MENU, self.OnHistMenu)
        return

    def __GetFlags(self):
        flags = 0
        data = self.GetSearchData()
        if data:
            flags = data.GetFlags()
        return flags

    def __SetFlags(self, flags):
        data = self.GetSearchData()
        if data:
            data.SetFlags(flags)

    SearchFlags = property(lambda self: self.__GetFlags(), lambda self, flags: self.__SetFlags(flags))

    def AutoSetQuery(self, multiline=False):
        """Autoload a selected string from the controls client buffer"""
        query = self.FindService.GetClientString(multiline)
        if len(query):
            self.FindService.SetQueryString(query)
            self.SetValue(query)

    def ClearSearchFlag(self, flag):
        """Clears a previously set search flag
        @param flag: flag to clear from search data

        """
        data = self.GetSearchData()
        if data is not None:
            c_flags = data.GetFlags()
            c_flags ^= flag
            self.SearchFlags = c_flags
            self.FindService.RefreshControls()
        return

    def FindAll(self):
        """Fire off a FindAll job in the current buffer"""
        evt = eclib.FindEvent(eclib.edEVT_FIND_ALL, flags=self.SearchFlags)
        evt.SetFindString(self.GetValue())
        self.FindService.OnFindAll(evt)

    def DoSearch(self, next=True, incremental=False):
        """Do the search and move the selection
        @keyword next: search next or previous
        @keyword incremental: is this an incremental search

        """
        s_cmd = eclib.edEVT_FIND
        if not next:
            self.SetSearchFlag(eclib.AFR_UP)
        elif eclib.AFR_UP & self.SearchFlags:
            self.ClearSearchFlag(eclib.AFR_UP)
        if self.GetValue() == self._last:
            s_cmd = eclib.edEVT_FIND_NEXT
        evt = eclib.FindEvent(s_cmd, flags=self.SearchFlags)
        self._last = self.GetValue()
        evt.SetFindString(self.GetValue())
        self.FindService.OnFind(evt, incremental=incremental)
        if self.FindService.GetLastFound() < 0 and len(self.GetValue()) > 0:
            if self._txtctrl is None:
                self.SetForegroundColour(wx.RED)
            else:
                self._txtctrl.SetForegroundColour(wx.RED)
            wx.Bell()
        elif self._txtctrl is None:
            self.SetForegroundColour(wx.ColourRGB(1))
        else:
            self._txtctrl.SetForegroundColour(wx.ColourRGB(1))
        self.Refresh()
        return

    def GetSearchController(self):
        """Get the L{SearchController} used by this control.
        @return: L{SearchController}

        """
        return self.FindService

    def GetSearchData(self):
        """Gets the find data from the controls FindService
        @return: wx.FindReplaceData

        """
        if hasattr(self.FindService, 'GetData'):
            return self.FindService.GetData()
        else:
            return
            return

    def GetHistory(self):
        """Gets and returns the history list of the control
        @return: list of recent search items

        """
        return getattr(self, '_recent', list())

    def InsertHistoryItem(self, value):
        """Inserts a search query value into the top of the history stack
        @param value: search string
        @postcondition: the value is added to the history menu

        """
        if value == wx.EmptyString:
            return
        m_items = list(self.rmenu.GetMenuItems())
        for menu_i in m_items:
            if value == menu_i.GetLabel():
                self.rmenu.RemoveItem(menu_i)

        n_item = wx.MenuItem(self.rmenu, wx.NewId(), value)
        self.rmenu.InsertItem(2, n_item)
        self._recent.insert(0, value)
        if len(self._recent) > self.max_menu:
            self._recent.pop()
        m_len = self.rmenu.GetMenuItemCount()
        if m_len > self.max_menu:
            try:
                self.rmenu.RemoveItem(m_items[(-1)])
            except IndexError, msg:
                wx.GetApp().GetLog()('[ed_search][err] menu error: %s' % str(msg))

    def IsMatchCase(self):
        """Returns True if the search control is set to search
        in Match Case mode.
        @return: whether search is using match case or not

        """
        data = self.GetSearchData()
        if data is not None:
            return bool(eclib.AFR_MATCHCASE & data.GetFlags())
        else:
            return False

    def IsRegEx(self):
        """Returns True if the search control is set to search
        in regular expression mode.
        @return: whether search is using regular expressions or not

        """
        data = self.GetSearchData()
        if data is not None:
            return bool(eclib.AFR_REGEX & data.GetFlags())
        else:
            return False

    def IsSearchPrevious(self):
        """Returns True if the search control is set to search
        in Previous mode.
        @return: whether search is searching up or not

        """
        data = self.GetSearchData()
        if data is not None:
            return bool(eclib.AFR_UP & data.GetFlags())
        else:
            return False

    def IsWholeWord(self):
        """Returns True if the search control is set to search
        in Whole Word mode.
        @return: whether search is using match whole word or not

        """
        data = self.GetSearchData()
        if data is not None:
            return bool(eclib.AFR_WHOLEWORD & data.GetFlags())
        else:
            return False

    def SetFocus(self):
        """Set the focus and select the text"""
        super(EdSearchCtrl, self).SetFocus()
        self.AutoSetQuery()
        self.SelectAll()

    def SetHistory(self, hist_list):
        """Populates the history list from a list of
        string values.
        @param hist_list: list of search items

        """
        hist_list.reverse()
        for item in hist_list:
            self.InsertHistoryItem(item)

    def SetSearchFlag(self, flags):
        """Sets the search data flags
        @param flags: search flag to add

        """
        data = self.GetSearchData()
        if data is not None:
            c_flags = data.GetFlags()
            c_flags |= flags
            self.SearchFlags = c_flags
            self.FindService.RefreshControls()
        return

    def ProcessEvent(self, evt):
        """Processes Events for the Search Control
        @param evt: the event that called this handler

        """
        e_key = evt.GetKeyCode()
        if evt.GetEventType() != wx.wxEVT_KEY_UP:
            if e_key in (wx.WXK_UP, wx.WXK_DOWN):
                buff = wx.GetApp().GetCurrentBuffer()
                if isinstance(buff, wx.stc.StyledTextCtrl):
                    val = -1
                    if e_key == wx.WXK_DOWN:
                        val = 1
                    buff.ScrollLines(val)
            else:
                evt.Skip()
            return
        if e_key == wx.WXK_ESCAPE:
            self.GetParent().Hide()
            evt.Skip()
            return
        if e_key == wx.WXK_SHIFT:
            self.ClearSearchFlag(eclib.AFR_UP)
            return
        tmp = self.GetValue()
        self.ShowCancelButton(len(tmp) > 0)
        if tmp == wx.EmptyString or evt.CmdDown() or evt.ControlDown() or e_key in [wx.WXK_COMMAND, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_CONTROL,
         wx.WXK_ALT, wx.WXK_UP, wx.WXK_DOWN, wx.WXK_F1, wx.WXK_F2,
         wx.WXK_F3, wx.WXK_F4, wx.WXK_F5, wx.WXK_F6, wx.WXK_F7,
         wx.WXK_F8, wx.WXK_F9, wx.WXK_F10, wx.WXK_F11, wx.WXK_F12]:
            return
        if e_key == wx.WXK_RETURN or e_key == wx.WXK_F3:
            if evt.ShiftDown():
                self.DoSearch(next=False)
            else:
                self.DoSearch(next=True)
            if e_key == wx.WXK_RETURN:
                self.InsertHistoryItem(self.GetValue())
        elif not self.IsRegEx():
            self.DoSearch(next=True, incremental=True)

    def OnCancel(self, evt):
        """Cancels the Search Query
        @param evt: SearchCtrl event

        """
        self.SetValue('')
        self.ShowCancelButton(False)
        evt.Skip()

    def OnHistMenu(self, evt):
        """Sets the search controls value to the selected menu item
        @param evt: wx.MenuEvent

        """
        item_id = evt.GetId()
        item = self.rmenu.FindItemById(item_id)
        if item != None:
            self.SetValue(item.GetLabel())
        else:
            evt.Skip()
        return


class EdFindResults(plugin.Plugin):
    """Shelf interface implementation for the find results"""
    plugin.Implements(iface.ShelfI)
    SUBSCRIBED = False
    RESULT_SCREENS = list()

    def __init__(self, pmgr):
        """Create the FindResults plugin
        @param pmgr: This plugins manager

        """
        if not EdFindResults.SUBSCRIBED:
            ed_msg.Subscribe(EdFindResults.StartResultsScreen, ed_msg.EDMSG_START_SEARCH)
            EdFindResults.SUBSCRIBED = True

    @property
    def __name__(self):
        return 'Find Results'

    def AllowMultiple(self):
        """Find Results allows multiple instances"""
        return True

    def CreateItem(self, parent):
        """Returns a log viewr panel"""
        screen = SearchResultScreen(parent)
        EdFindResults.RESULT_SCREENS.append(screen)
        return screen

    def GetBitmap(self):
        """Get the find results bitmap
        @return: wx.Bitmap

        """
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_FIND), wx.ART_MENU)
        return bmp

    def GetId(self):
        """Plugin menu identifier ID"""
        return ed_glob.ID_FIND_RESULTS

    def GetMenuEntry(self, menu):
        """Get the menu entry for the log viewer
        @param menu: the menu items parent menu

        """
        return

    def GetName(self):
        """Return the name of this control"""
        return self.__name__

    def IsStockable(self):
        """EdFindResults can be saved in the shelf preference stack"""
        return False

    @classmethod
    def StartResultsScreen(cls, msg):
        """Start a search in an existing window or open a new one
        @param cls: this class
        @param msg: message object

        """
        win = wx.GetApp().GetActiveWindow()
        to_pop = list()
        for (idx, item) in enumerate(list(EdFindResults.RESULT_SCREENS)):
            if not isinstance(item, SearchResultScreen):
                to_pop.append(idx)

        for idx in reversed(to_pop):
            EdFindResults.RESULT_SCREENS.pop(idx)

        screen = None
        if win is not None:
            shelf = win.GetShelf()
            s_mw = shelf.GetOwnerWindow()
            shelf_nb = shelf.GetWindow()
            for item in EdFindResults.RESULT_SCREENS:
                if item.GetDisplayedLines() < 3 and s_mw is win and item.GetParent() is shelf_nb:
                    screen = shelf.RaiseWindow(item)
                    break

            if screen is None:
                shelf.PutItemOnShelf(ed_glob.ID_FIND_RESULTS)
                screen = shelf_nb.GetCurrentPage()
            data = msg.GetData()
            if len(data) > 1:
                screen.StartSearch(data[0], *data[1], **data[2])
            else:
                screen.StartSearch(data[0])
        return


class SearchResultScreen(ed_basewin.EdBaseCtrlBox):
    """Screen for displaying search results and navigating to them"""

    def __init__(self, parent):
        """Create the result screen
        @param parent: parent window

        """
        super(SearchResultScreen, self).__init__(parent)
        self._meth = None
        self._job = None
        self._list = SearchResultList(self)
        self._cancelb = None
        self._clearb = None
        self.__DoLayout()
        self._cancelb.Disable()
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy, self)
        self.Bind(wx.EVT_BUTTON, lambda evt: self._list.Clear(), self._clearb)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.CancelSearch(), self._cancelb)
        self._list.Bind(eclib.EVT_TASK_START, self.OnTaskStart)
        self._list.Bind(eclib.EVT_TASK_COMPLETE, self.OnTaskComplete)
        ed_msg.Subscribe(self.OnThemeChange, ed_msg.EDMSG_THEME_CHANGED)
        return

    def OnDestroy(self, evt):
        if evt.Id == self.Id:
            ed_msg.Unsubscribe(self.OnThemeChange)
        evt.Skip()

    def __DoLayout(self):
        """Layout and setup the results screen ui"""
        ctrlbar = self.CreateControlBar(wx.TOP)
        ctrlbar.AddStretchSpacer()
        cancel = self.AddPlateButton(_('Cancel'), ed_glob.ID_STOP, wx.ALIGN_RIGHT)
        self._cancelb = cancel
        clear = self.AddPlateButton(_('Clear'), ed_glob.ID_DELETE, wx.ALIGN_RIGHT)
        self._clearb = clear
        self.SetWindow(self._list)

    def GetDisplayedLines(self):
        """Get the number of lines displayed in the output window"""
        return self._list.GetLineCount()

    def OnTaskStart(self, evt):
        """Start accepting results from the search thread
        @param evt: UpdateBufferEvent

        """
        start = '>>> %s' % _('Search Started')
        if self._meth is not None:
            start += ': ' + self._meth.im_self.GetOptionsString()
        self._list.SetStartEndText(start + os.linesep)
        self._list.Start(250)
        return

    def OnTaskComplete(self, evt):
        """Update when task is complete
        @param evt: UpdateBufferEvent

        """
        self._meth = None
        self._list.Stop()
        self._cancelb.Disable()
        ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT, (
         ed_glob.SB_INFO, _('Search complete')))
        self._list.FlushBuffer()
        lines = max(0, self._list.GetLineCount() - 2)
        msg = _('Search Complete: %d matching lines where found.') % lines
        msg2 = _('Files Searched: %d' % self._list.GetFileCount())
        end = '>>> %s \t%s' % (msg, msg2)
        self._list.SetStartEndText(end + os.linesep)
        return

    def OnThemeChange(self, msg):
        """Update the button icons after the theme has changed
        @param msg: Message Object

        """
        cbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_DELETE), wx.ART_MENU)
        self._clearb.SetBitmap(cbmp)
        self._clearb.Refresh()
        cbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_STOP), wx.ART_MENU)
        self._cancelb.SetBitmap(cbmp)
        self._cancelb.Refresh()

    def CancelSearch(self):
        """Cancel the currently running search"""
        if self._job is not None:
            self._job.Cancel()
        self._cancelb.Disable()
        return

    def StartSearch(self, searchmeth, *args, **kwargs):
        """Start a search with the given method and display the results
        @param searchmeth: callable
        @param *args: positional arguments to pass to searchmeth
        @param **kwargs: keyword arguments to pass to searchmeth

        """
        self._meth = searchmeth
        if self._job is not None:
            self._job.Cancel()
        self._list.Clear()
        self._job = eclib.TaskObject(self._list, searchmeth, *args, **kwargs)
        ed_thread.EdThreadPool().QueueJob(self._job.DoTask)
        self._cancelb.Enable()
        return


class SearchResultList(eclib.OutputBuffer):
    """Outputbuffer for listing matching lines from the search results that
    a L{ebmlib.SearchEngine} dispatches. The matching lines are turned into
    hotspots that allow them to be clicked on for instant navigation to the
    matching line.

    """
    STY_SEARCH_MATCH = eclib.OPB_STYLE_MAX + 1
    RE_FIND_MATCH = re.compile('(.+) \\(([0-9]+)\\)\\: .+')

    def __init__(self, parent):
        super(SearchResultList, self).__init__(parent)
        self._files = 0
        font = Profile_Get('FONT1', 'font', wx.Font(11, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.SetFont(font)
        style = (font.GetFaceName(), font.GetPointSize(), '#FFFFFF')
        self.StyleSetSpec(SearchResultList.STY_SEARCH_MATCH, 'face:%s,size:%d,fore:#000000,back:%s' % style)
        self.StyleSetHotSpot(SearchResultList.STY_SEARCH_MATCH, True)

    def AppendUpdate(self, value):
        """Do a little filtering of updates as they arrive
        @param value: search result from search method

        """
        if isinstance(value, basestring):
            super(SearchResultList, self).AppendUpdate(value)
        else:
            self._files += 1
            if self._files == 1 or self._files / 10 > (self._files - 1) / 10:
                wx.CallAfter(ed_msg.PostMessage, ed_msg.EDMSG_UI_SB_TXT, (
                 ed_glob.SB_INFO,
                 value[1]))

    def ApplyStyles(self, start, txt):
        """Set a hotspot for each search result
        Search matches strings should be formatted as follows
        /file/name (line) match string
        @param start: long
        @param txt: string

        """
        self.StartStyling(start, 31)
        if re.match(SearchResultList.RE_FIND_MATCH, txt):
            self.SetStyling(len(txt), SearchResultList.STY_SEARCH_MATCH)
        else:
            self.SetStyling(len(txt), eclib.OPB_STYLE_DEFAULT)

    def Clear(self):
        """Override OutputBuffer.Clear"""
        self._files = 0
        super(SearchResultList, self).Clear()

    def DoHotSpotClicked(self, pos, line):
        """Handle a click on a hotspot and open the file to the matched line
        @param pos: long
        @param line: int

        """
        txt = self.GetLine(line)
        match = re.match(SearchResultList.RE_FIND_MATCH, txt)
        if match is not None:
            groups = match.groups()
            if len(groups) == 2:
                (fname, lnum) = groups
                if lnum.isdigit():
                    lnum = int(lnum) - 1
                else:
                    lnum = 0
                self._OpenToLine(fname, lnum)
        return

    def GetFileCount(self):
        """Get the number of files searched in the previous/current search job.
        @return: int

        """
        return self._files

    def SetStartEndText(self, txt):
        """Add a start task or end task message to the output. Styled in
        Info style.
        @param txt: text to add

        """
        self.SetReadOnly(False)
        cpos = self.GetLength()
        self.AppendText(txt)
        self.StartStyling(cpos, 31)
        self.SetStyling(self.GetLength() - cpos, eclib.OPB_STYLE_INFO)
        self.SetReadOnly(True)

    @staticmethod
    def _OpenToLine(fname, line):
        """Open the given filename to the given line number
        @param fname: File name to open, relative paths will be converted to abs
                      paths.
        @param line: Line number to set the cursor to after opening the file

        """
        mainw = wx.GetApp().GetActiveWindow()
        nbook = mainw.GetNotebook()
        buffers = [ page.GetFileName() for page in nbook.GetTextControls() ]
        if fname in buffers:
            page = buffers.index(fname)
            nbook.ChangePage(page)
            cpage = nbook.GetPage(page)
        else:
            nbook.OnDrop([fname])
            cpage = nbook.GetPage(nbook.GetSelection())
        cpage.GotoLine(line)
        cpage.SetFocus()