# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_pages.py
# Compiled at: 2012-08-12 13:42:45
"""
This class implements Editra's main notebook control.
@summary: Editra's main notebook class

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_pages.py 72278 2012-08-02 14:24:23Z CJP $'
__revision__ = '$Revision: 72278 $'
import os, sys, glob, wx, ed_glob
from profiler import Profile_Get, Profile_Set
import ed_editv, syntax.synglob as synglob, syntax.syntax, ed_search, util, ed_msg, ed_txt, ed_mdlg, ed_session, ebmlib, eclib
from extern import aui
import ed_book
ID_IDLE_TIMER = wx.NewId()
SIMULATED_EVT_ID = -1
_ = wx.GetTranslation

class EdPages(ed_book.EdBaseBook):
    """Editra's editor buffer notebook
    @todo: allow for tab styles to be configurable (maybe)

    """

    def __init__(self, parent):
        """Initialize a notebook with a blank text control in it
        @param parent: parent window of the notebook

        """
        style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_WINDOWLIST_BUTTON | aui.AUI_NB_SMART_TABS | aui.AUI_NB_USE_IMAGES_DROPDOWN | aui.AUI_NB_TAB_EXTERNAL_MOVE | aui.AUI_NB_TAB_FIXED_WIDTH | aui.AUI_NB_ORDER_BY_ACCESS
        super(EdPages, self).__init__(parent, style=style)
        self.LOG = wx.GetApp().GetLog()
        self._idletimer = wx.Timer(self, ID_IDLE_TIMER)
        self.DocMgr = ed_editv.EdEditorView.DOCMGR
        self._searchctrl = ed_search.SearchController(self, self.GetCurrentCtrl)
        self._searchctrl.SetLookinChoices(Profile_Get('SEARCH_LOC', default=list()))
        self._searchctrl.SetFileFilters(Profile_Get('SEARCH_FILTER', default=''))
        self.pg_num = -1
        self.mdown = -1
        self.control = None
        self.frame = self.GetTopLevelParent()
        self._ses_load = False
        self._menu = ebmlib.ContextMenuManager()
        ed_icon = ed_glob.CONFIG['SYSPIX_DIR'] + 'editra.png'
        bmp = wx.Bitmap(ed_icon, wx.BITMAP_TYPE_PNG)
        if bmp.IsOk():
            self.SetNavigatorIcon(bmp)
        else:
            util.Log('[ed_pages][warn] Bad bitmap: %s' % ed_icon)
        self.SetMinMaxTabWidth(125, 135)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy, self)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnPageClosing)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.OnPageClosed)
        self.Bind(aui.EVT_AUINOTEBOOK_TAB_DCLICK, self.OnTabLeftDClick)
        self.Bind(aui.EVT_AUINOTEBOOK_BG_DCLICK, self.OnBGLeftDClick)
        self.Bind(aui.EVT_AUINOTEBOOK_TAB_MIDDLE_DOWN, self.OnMClickDown)
        self.Bind(aui.EVT_AUINOTEBOOK_TAB_MIDDLE_UP, self.OnMClickUp)
        self.Bind(aui.EVT_AUINOTEBOOK_TAB_RIGHT_UP, self.OnTabMenu)
        self.Bind(aui.EVT_AUINOTEBOOK_ALLOW_DND, self.OnAllowDnD)
        self.Bind(aui.EVT_AUINOTEBOOK_END_DRAG, self.OnDragFinished)
        self.Bind(aui.EVT_AUINOTEBOOK_DRAG_DONE, self.OnDragFinished)
        self.Bind(wx.stc.EVT_STC_CHANGE, self.OnUpdatePageText)
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_TIMER, self.OnIdle, id=ID_IDLE_TIMER)
        ed_msg.Subscribe(self.OnThemeChanged, ed_msg.EDMSG_THEME_CHANGED)
        ed_msg.Subscribe(self.OnThemeChanged, ed_msg.EDMSG_THEME_NOTEBOOK)
        ed_msg.Subscribe(self.OnUpdatePosCache, ed_msg.EDMSG_UI_STC_POS_JUMPED)
        ed_msg.Subscribe(self.OnGetOpenFiles, ed_msg.EDMSG_FILE_GET_OPENED)
        ed_msg.RegisterCallback(self.OnDocPointerRequest, ed_msg.EDREQ_DOCPOINTER)
        self.NewPage()
        self._idletimer.Start(400)
        return

    def OnDestroy(self, evt):
        if self and evt.Id == self.Id:
            ed_msg.Unsubscribe(self.OnThemeChanged)
            ed_msg.Unsubscribe(self.OnUpdatePosCache)
            ed_msg.Unsubscribe(self.OnGetOpenFiles)
            ed_msg.UnRegisterCallback(self.OnDocPointerRequest)

    def _HandleEncodingError(self, control):
        """Handle trying to reload the file the file with a different encoding
        Until it succeeds or gives up.
        @param control: stc
        @return: bool

        """
        tried = None
        fname = control.GetFileName().strip(os.sep)
        fname = fname.split(os.sep)[(-1)]
        while True:
            doc = control.GetDocument()
            doc.ClearLastError()
            if tried is None:
                enc = doc.GetEncoding()
                if enc is None:
                    enc = ed_txt.DEFAULT_ENCODING
            else:
                enc = tried
            msg = _("The correct encoding of '%s' could not be determined.\n\nChoose an encoding and select Ok to open the file with the chosen encoding.\nClick Cancel to abort opening the file") % fname
            if enc is None:
                enc = 'utf_8'
            dlg = eclib.EncodingDialog(self, msg=msg, title=_('Choose an Encoding'), default=enc)
            bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_DOCPROP), wx.ART_OTHER)
            if bmp.IsOk():
                dlg.SetBitmap(bmp)
            dlg.CenterOnParent()
            result = dlg.ShowModal()
            if dlg:
                enc = dlg.GetEncoding()
                dlg.Destroy()
            else:
                result = wx.ID_CANCEL
            if result == wx.ID_CANCEL:
                return False
            control.SetEncoding(enc)
            tried = enc
            ok = control.LoadFile(control.GetFileName())
            if ok:
                return True
            wx.Sleep(1)

        return

    def _NeedOpen(self, path):
        """Check if a file needs to be opened. If the file is already open in
        the notebook a dialog will be opened to ask if the user wants to reopen
        the file again. If the file is not open and exists or the user chooses
        to reopen the file again the function will return True else it will
        return False.
        @param path: file to check for
        @return: bool

        """
        result = wx.ID_YES
        if self.HasFileOpen(path):
            mdlg = wx.MessageDialog(self, _('File is already open in an existing page.\nDo you wish to open it again?'), _('Open File') + '?', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
            result = mdlg.ShowModal()
            mdlg.Destroy()
            if result == wx.ID_NO:
                self.GotoPage(path)
        elif os.path.exists(path) and not os.path.isfile(path):
            result = wx.ID_NO
        return result == wx.ID_YES

    def AddPage(self, page, text='', select=True, imgId=-1):
        """Add a page to the notebook"""
        bNewPage = False
        if not len(text):
            self.pg_num += 1
            if self.pg_num != 0:
                text = _('untitled %d') % self.pg_num
            else:
                text = _('untitled')
            bNewPage = True
        page.SetTabLabel(text)
        bmp = wx.NullBitmap
        if Profile_Get('TABICONS'):
            bmp = page.GetTabImage()
        super(EdPages, self).AddPage(page, text, select, bitmap=bmp)
        self.UpdateIndexes()
        if not self._ses_load and not bNewPage:
            mgr = ed_session.EdSessionMgr()
            if Profile_Get('LAST_SESSION') == mgr.DefaultSession:
                self.SaveCurrentSession()

    def DocDuplicated(self, path):
        """Check for if the given path is open elsewhere and duplicate the
        docpointer.
        @param path: string

        """
        doc = ed_msg.RequestResult(ed_msg.EDREQ_DOCPOINTER, [self, path])
        if hasattr(doc, 'GetDocPointer'):
            self.OpenDocPointer(doc.GetDocPointer(), doc.GetDocument())
            return True
        else:
            return False

    def GetCurrentCtrl(self):
        """Returns the control of the currently selected
        page in the notebook.
        @return: window object contained in current page or None

        """
        return self.control

    def GetFileNames(self):
        """Gets the name of all open files in the notebook
        @return: list of file names

        """
        rlist = list()
        for buff in self.GetTextControls():
            fname = buff.GetFileName()
            if fname != wx.EmptyString:
                rlist.append(fname)

        return rlist

    def GetFindDialog(self):
        """Get the active find dialog or None if one is not active
        @return: FindDialog or None

        """
        return self._searchctrl.GetDialog()

    def GetMenuHandlers(self):
        """Get the (id, evt_handler) tuples that this window should
        handle.
        @return: list of tuples

        """
        rlist = [
         (
          ed_glob.ID_FIND, self._searchctrl.OnShowFindDlg),
         (
          ed_glob.ID_FIND_REPLACE, self._searchctrl.OnShowFindDlg),
         (
          ed_glob.ID_FIND_NEXT, self._searchctrl.OnFind),
         (
          ed_glob.ID_FIND_PREVIOUS, self._searchctrl.OnFind),
         (
          ed_glob.ID_FIND_SELECTED, self._searchctrl.OnFindSelected),
         (
          ed_glob.ID_NEXT_POS, self.OnNavigateToPos),
         (
          ed_glob.ID_PRE_POS, self.OnNavigateToPos)]
        return rlist

    def GetUiHandlers(self):
        """Get the update ui handlers that this window supplies
        @return: list of tuples

        """
        return [
         (
          ed_glob.ID_FIND_NEXT, self._searchctrl.OnUpdateFindUI),
         (
          ed_glob.ID_FIND_PREVIOUS, self._searchctrl.OnUpdateFindUI),
         (
          ed_glob.ID_NEXT_POS, self.OnUpdateNaviUI),
         (
          ed_glob.ID_PRE_POS, self.OnUpdateNaviUI)]

    def InsertPage(self, index, page, text, select=False, bitmap=wx.NullBitmap, disabled_bitmap=wx.NullBitmap, control=None):
        """Insert a page into the notebook"""
        super(EdPages, self).InsertPage(index, page, text, select, bitmap, disabled_bitmap, control)
        self.UpdateIndexes()

    def SaveCurrentSession(self):
        """Save the current session"""
        if self._ses_load:
            return
        session = Profile_Get('LAST_SESSION')
        if not isinstance(session, basestring) or not len(session):
            mgr = ed_session.EdSessionMgr()
            session = mgr.DefaultSession
            Profile_Set('LAST_SESSION', session)
        self.SaveSessionFile(session)

    def SaveSessionFile(self, session):
        """Save the current open files to the given session file
        @param session: path to session file
        @return: tuple (error desc, error msg) or None

        """
        if self._ses_load:
            return
        else:
            try:
                mgr = ed_session.EdSessionMgr()
                flist = self.GetFileNames()
                bSaved = mgr.SaveSession(session, flist)
            except Exception, msg:
                self.LOG('[ed_pages][err] SaveSession error %s' % msg)

            return

    def LoadSessionFile(self, session):
        """Load files from saved session data in profile
        @param session: session filename
        @return: tuple (error desc, error msg), or None if no error

        """
        self._ses_load = True
        mgr = ed_session.EdSessionMgr()
        flist = list()
        try:
            flist = mgr.LoadSession(session)
        except Exception, msg:
            self._ses_load = False
            errdict = dict(sessionname=session, error=msg)
            return (_('Session Load Error'),
             _('Failed to load the session: %(sessionname)s\n\nError: %(error)s') % errdict)

        if not len(flist):
            self._ses_load = False
            return (
             _('Empty File'), _('Session file is empty.'))
        else:
            self.CloseAllPages()
            missingfns = []
            for loadfn in flist:
                if os.path.exists(loadfn) and os.access(loadfn, os.R_OK):
                    if not ebmlib.IsUnicode(loadfn):
                        try:
                            loadfn = loadfn.decode(sys.getfilesystemencoding())
                        except UnicodeDecodeError:
                            self.LOG('[ed_pages][err] LoadSessionFile: Failed to decode file name')

                    self.OpenPage(os.path.dirname(loadfn), os.path.basename(loadfn))
                else:
                    missingfns.append(loadfn)

            if missingfns:
                rmsg = (
                 _('Missing session files'),
                 _('Some files in saved session could not be found on disk:\n') + ('\n').join(missingfns))
                self._ses_load = False
                return rmsg
            self._ses_load = False
            if self.GetPageCount() == 0:
                self.NewPage()
            self.Refresh()
            return

    def NewPage(self):
        """Create a new notebook page with a blank text control
        @postcondition: a new page with an untitled document is opened

        """
        frame = self.TopLevelParent
        with eclib.Freezer(frame) as (_tmp):
            self.control = ed_editv.EdEditorView(self)
            self.LOG('[ed_pages][evt] New Page Created')
            self.AddPage(self.control)
        dlexer = Profile_Get('DEFAULT_LEX', 'str', synglob.LANG_TXT)
        ext_reg = syntax.ExtensionRegister()
        ext_lst = ext_reg.get(dlexer, ['txt'])
        self.control.FindLexer(ext_lst[0])
        self.SetPageBitmap(self.GetSelection(), self.control.GetTabImage())
        doc = self.control.GetDocument()
        doc.AddModifiedCallback(self.control.FireModified)

    def OnAllowDnD(self, evt):
        """Handle allowing tab drag and drop events"""
        dsource = evt.GetDragSource()
        if isinstance(dsource, EdPages):
            evt.Allow()
            wx.CallAfter(self.UpdateIndexes)

    def OnDragFinished(self, evt):
        self.UpdateIndexes()
        evt.Skip()

    def OnMenu(self, evt):
        """Handle context menu events
        @param evt: wx.MenuEvent

        """
        ctab = self.GetCurrentPage()
        handler = self._menu.GetHandler(evt.Id)
        if handler is not None:
            handler(ctab, evt)
        elif ctab is not None:
            ctab.OnTabMenu(evt)
        else:
            evt.Skip()
        return

    def OnDocPointerRequest(self, args):
        """Get a buffer that has the same file open as the requested path.
        @param args: [sender, path]
        @return: EdEditorView reference or ed_msg.NullValue

        """
        (sender, path) = args
        for buf in self.GetTextControls():
            if buf.GetFileName() == path:
                return buf
        else:
            return ed_msg.NullValue()

    def OnTabLeftDClick(self, evt):
        """Handle left double clicks and open new tab when in empty area.
        @param evt: aui.EVT_AUINOTEBOOK_TAB_DCLICK

        """
        tlw = self.GetTopLevelParent()
        if hasattr(tlw, 'OnMaximizeEditor'):
            tlw.OnMaximizeEditor(None)
        return

    def OnBGLeftDClick(self, evt):
        """Handle clicks on tab background area
        @param evt: aui.EVT_AUINOTEBOOK_BG_DCLICK

        """
        self.NewPage()

    def OnMClickDown(self, evt):
        """Handle tab middle mouse button down click event
        @param evt: aui.EVT_AUINOTEBOOK_TAB_MIDDLE_DOWN

        """
        self.mdown = evt.Page
        idx = self.GetPageIndex(self.mdown)
        self.SetSelection(idx)
        self.LOG('[ed_pages][evt] OnMClickDown: %d' % idx)

    def OnMClickUp(self, evt):
        """Handle tab middle click event
        @param evt: aui.EVT_AUINOTEBOOK_TAB_MIDDLE_UP

        """
        sel = self.GetPageIndex(evt.Page)
        self.LOG('[ed_pages][evt] OnMClickUp: %d' % sel)
        if evt.Page is self.mdown:
            self.ClosePage()
        self.mdown = None
        return

    def OnNavigateToPos(self, evt):
        """Handle buffer position history navigation events"""
        e_id = evt.GetId()
        (fname, pos) = (None, None)
        cname = self.control.GetFileName()
        cpos = self.control.GetCurrentPos()
        if e_id == ed_glob.ID_NEXT_POS:
            if self.DocMgr.CanNavigateNext():
                (fname, pos) = self.DocMgr.GetNextNaviPos()
                if (fname, pos) == (cname, cpos):
                    (fname, pos) = (None, None)
                    tmp = self.DocMgr.GetNextNaviPos()
                    if tmp is not None:
                        (fname, pos) = tmp
        elif e_id == ed_glob.ID_PRE_POS:
            if self.DocMgr.CanNavigatePrev():
                (fname, pos) = self.DocMgr.GetPreviousNaviPos()
                if (fname, pos) == (cname, cpos):
                    (fname, pos) = (None, None)
                    tmp = self.DocMgr.GetPreviousNaviPos()
                    if tmp is not None:
                        (fname, pos) = tmp
        else:
            evt.Skip()
            return
        ctrl = self.FindBuffer(fname)
        if ctrl is None:
            if fname is not None:
                self.OpenPage(ebmlib.GetPathName(fname), ebmlib.GetFileName(fname))
                self.control.SetCaretPos(pos)
        else:
            pages = [ self.GetPage(page) for page in range(self.GetPageCount()) ]
            idx = pages.index(ctrl)
            self.ChangePage(idx)
            ctrl.SetCaretPos(pos)
        return

    def OnTabMenu(self, evt):
        """Show the tab context menu"""
        self._menu.Clear()
        tab = self.GetPageIndex(evt.Page)
        if tab != self.GetSelection():
            self.SetSelection(tab)
        ctab = self.GetCurrentPage()
        if ctab is not None:
            menu = ctab.GetTabMenu()
            if menu is None:
                return
            self._menu.SetMenu(menu)
            self._menu.SetUserData('page', ctab)
            ed_msg.PostMessage(ed_msg.EDMSG_UI_NB_TABMENU, self._menu)
            self.PopupMenu(self._menu.Menu)
        return

    def GetMainWindow(self):
        return self.TopLevelParent

    @ed_msg.mwcontext
    def OnGetOpenFiles(self, msg):
        """Report all opened files"""
        if not self:
            return
        data = msg.GetData()
        if not isinstance(data, list):
            return
        flist = self.GetFileNames()
        data.extend(flist)

    def OnThemeChanged(self, msg):
        """Update icons when the theme has changed
        @param msg: Message Object

        """
        self.UpdateAllImages()

    def OnUpdatePosCache(self, msg):
        """Update the position cache for buffer position changes
        @param msg: message data

        """
        if not self or self._ses_load:
            return
        if self.TopLevelParent.Id == msg.GetContext():
            data = msg.GetData()
            self.DocMgr.AddNaviPosition(data['fname'], data['prepos'])
            self.DocMgr.AddNaviPosition(data['fname'], data['pos'])

    def OnUpdateNaviUI(self, evt):
        """UpdateUI handler for position navigator"""
        e_id = evt.Id
        if e_id == ed_glob.ID_NEXT_POS:
            evt.Enable(self.DocMgr.CanNavigateNext())
        elif e_id == ed_glob.ID_PRE_POS:
            evt.Enable(self.DocMgr.CanNavigatePrev())
        else:
            evt.Skip()

    def OpenDocPointer(self, ptr, doc, title=''):
        """Open a page using an stc document poiner
        @param ptr: EdEditorView document Pointer
        @param doc: EdFile instance
        @keyword title: tab title

        """
        with eclib.Freezer(self.TopLevelParent) as (_tmp):
            nbuff = self.GetCurrentPage()
            need_add = False
            if nbuff.GetFileName() or nbuff.GetLength():
                need_add = True
                nbuff = ed_editv.EdEditorView(self)
            nbuff.SetDocPointer(ptr)
            nbuff.SetDocument(doc)
            doc.AddModifiedCallback(nbuff.FireModified)
            nbuff.FindLexer()
            path = nbuff.GetFileName()
            if Profile_Get('SAVE_POS'):
                pos = self.DocMgr.GetPos(path)
                nbuff.SetCaretPos(pos)
                nbuff.ScrollToColumn(0)
            if title:
                filename = title
            else:
                filename = ebmlib.GetFileName(path)
            if need_add:
                self.AddPage(nbuff, filename)
            else:
                self.SetPageText(self.GetSelection(), filename)
            self.LOG('[ed_pages][evt] Opened Page: %s' % filename)
            self.SetPageBitmap(self.GetSelection(), nbuff.GetTabImage())
            self.control = nbuff
            self.GoCurrentPage()
            ed_msg.PostMessage(ed_msg.EDMSG_FILE_OPENED, nbuff.GetFileName(), context=self.frame.Id)

    def OpenFileObject(self, fileobj):
        """Open a new text editor page with the given file object. The file
        object must be an instance of ed_txt.EdFile.
        @param fileobj: File Object

        """
        with eclib.Freezer(self.TopLevelParent) as (_tmp):
            control = ed_editv.EdEditorView(self)
            control.Hide()
            path = fileobj.GetPath()
            filename = ebmlib.GetFileName(path)
            control.SetDocument(fileobj)
            result = control.ReloadFile()
            fileobj.AddModifiedCallback(control.FireModified)
            self.control = control
            self.control.FindLexer()
            self.control.EmptyUndoBuffer()
            self.control.Show()
            self.AddPage(self.control, filename)
            self.frame.AddFileToHistory(path)
            self.SetPageText(self.GetSelection(), filename)
            self.LOG('[ed_pages][evt] Opened Page: %s' % filename)
            cpage = self.GetSelection()
            self.SetPageBitmap(cpage, self.control.GetTabImage())
        self.GoCurrentPage()
        ed_msg.PostMessage(ed_msg.EDMSG_FILE_OPENED, self.control.GetFileName(), context=self.frame.Id)
        if Profile_Get('WARN_EOL', default=True) and not fileobj.IsRawBytes():
            self.control.CheckEOL()

    def OpenPage(self, path, filename, quiet=False):
        """Open a File Inside of a New Page
        @param path: files base path
        @param filename: name of file to open
        @keyword quiet: Open/Switch to the file quietly if
                        it is already open.

        """
        path2file = os.path.join(path, filename)
        if ebmlib.IsLink(path2file):
            path2file = ebmlib.ResolveRealPath(path2file)
            path = ebmlib.GetPathName(path2file)
            filename = ebmlib.GetFileName(path2file)
        if self.DocDuplicated(path2file):
            return
        if quiet and self.HasFileOpen(path2file):
            self.GotoPage(path2file)
            return
        if not self._NeedOpen(path2file):
            return
        with eclib.Freezer(self.TopLevelParent) as (_tmp):
            new_pg = True
            if self.GetPageCount():
                if self.control.GetModify() or self.control.GetLength() or self.control.GetFileName() != '':
                    control = ed_editv.EdEditorView(self, wx.ID_ANY)
                    control.Hide()
                else:
                    new_pg = False
                    control = self.control
            else:
                control = ed_editv.EdEditorView(self, wx.ID_ANY)
                control.Hide()
            result = False
            if os.path.exists(path2file):
                try:
                    result = control.LoadFile(path2file)
                except Exception, msg:
                    self.LOG('[ed_pages][err] Failed to open file %s\n' % path2file)
                    self.LOG('[ed_pages][err] %s' % msg)
                    if not self._ses_load:
                        ed_mdlg.OpenErrorDlg(self, path2file, msg)
                    control.GetDocument().ClearLastError()
                    control.SetFileName('')
                    if new_pg:
                        control.Destroy()
                    return

            else:
                control.SetFileName(path2file)
                result = True
            if not result and not self._ses_load:
                result = self._HandleEncodingError(control)
            if not result:
                if new_pg:
                    control.Destroy()
                else:
                    control.SetText('')
                    control.SetDocument(ed_txt.EdFile())
                    control.SetSavePoint()
                return
            if new_pg:
                control.Show()
                self.control = control
            self.control.FindLexer()
            self.control.EmptyUndoBuffer()
            doc = self.control.GetDocument()
            doc.AddModifiedCallback(self.control.FireModified)
            if new_pg:
                self.AddPage(self.control, filename)
            else:
                self.frame.SetTitle(self.control.GetTitleString())
            self.frame.AddFileToHistory(path2file)
            self.SetPageText(self.GetSelection(), filename)
            cpage = self.GetSelection()
            self.SetPageBitmap(cpage, self.control.GetTabImage())
            if Profile_Get('WARN_EOL', default=True) and not doc.IsRawBytes():
                self.control.CheckEOL()
            if not control.IsLoading():
                self.DoPostLoad()
            self.GoCurrentPage()
            self.LOG('[ed_pages][evt] Opened Page: %s' % filename)

    def DoPostLoad(self):
        """Perform post file open actions"""
        doc = self.control.GetDocument()
        if not doc.IsReadOnly() and not doc.IsRawBytes():
            self.control.SetReadOnly(False)
        if Profile_Get('SAVE_POS') and self.control.GetCurrentPos() <= 0:
            pos = self.DocMgr.GetPos(self.control.GetFileName())
            self.control.SetCaretPos(pos)
            self.control.ScrollToColumn(0)
        ed_msg.PostMessage(ed_msg.EDMSG_FILE_OPENED, self.control.GetFileName(), context=self.frame.Id)

    def GoCurrentPage(self):
        """Move Focus to Currently Selected Page.
        @postcondition: focus is set to current page

        """
        current_page = self.GetSelection()
        if current_page >= 0:
            control = self.GetPage(current_page)
            self.control = control
        return current_page

    def GotoPage(self, fname):
        """Go to the page containing the buffer with the given file.
        @param fname: file path (string)

        """
        for page in xrange(self.GetPageCount()):
            ctrl = self.GetPage(page)
            if fname == ctrl.GetFileName():
                self.ChangePage(page)
                break

    def GetPageText(self, pg_num):
        """Gets the tab text from the given page number, stripping
        the * mark if there is one.
        @param pg_num: index of page to get tab text from
        @return: the tabs text

        """
        try:
            txt = super(EdPages, self).GetPageText(pg_num)
        except Exception:
            txt = ''

        if not txt or txt[0] != '*':
            return txt
        return txt[1:]

    def GetRawPageText(self, pg_num):
        """Get the unformatted raw page text
        @param pg_num: int
        @return: string

        """
        try:
            txt = super(EdPages, self).GetPageText(pg_num)
        except Exception:
            txt = ''

        return txt

    def ImageIsReadOnly(self, index):
        """Does the given page currently have a ReadOnly Image
        shown on it?
        @return: bool

        """
        bReadOnly = False
        try:
            if index < self.GetPageCount():
                bReadOnly = self.GetPageImage(index) == self._index[ed_glob.ID_READONLY]
            else:
                self.LOG('[ed_pages][warn] ImageIsReadOnly: Bad index: %d' % index)
        except Exception, msg:
            self.LOG('[ed_pages][err] ImageIsReadOnly: %s' % msg)

        return bReadOnly

    def SetPageText(self, pg_num, txt):
        """Set the pages tab text
        @param pg_num: page index
        @param txt: string

        """
        super(EdPages, self).SetPageText(pg_num, txt)
        page = self.GetPage(pg_num)
        page.SetTabLabel(txt)

    def GetTextControls(self):
        """Gets all the currently opened text controls
        @return: list containing reference to all stc controls opened in the
                 notebook.

        """
        pages = [ self.GetPage(page) for page in xrange(self.GetPageCount()) ]
        return [ page for page in pages if page.GetName() == 'EditraTextCtrl' ]

    def HasFileOpen(self, fpath):
        """Checks if one of the currently active buffers has
        the named file in it.
        @param fpath: full path of file to check
        @return: bool indicating whether file is currently open or not

        """
        for ctrl in self.GetTextControls():
            if fpath == ctrl.GetFileName():
                return True

        return False

    def FindBuffer(self, fpath):
        """Find the buffer containing the given file
        @param fpath: full path of file to look for
        @return: EdStc or None
        @todo: handle matching based on the buffer control itself

        """
        for ctrl in self.GetTextControls():
            if fpath == ctrl.GetFileName():
                return ctrl

        return

    def OnDrop(self, files):
        """Opens dropped files
        @param files: list of file paths
        @postcondition: all files that could be properly opend are added to
                        the notebook

        """
        valid_files = list()
        for fname in files:
            self.LOG('[ed_pages][evt] File(s) Dropped: %s' % fname)
            if not os.path.exists(fname):
                self.frame.PushStatusText(_('Invalid file: %s') % fname, ed_glob.SB_INFO)
            elif os.path.isdir(fname):
                dcnt = glob.glob(os.path.join(fname, '*'))
                dcnt = util.FilterFiles(dcnt)
                dlg = None
                if not len(dcnt):
                    dlg = wx.MessageDialog(self, _('There are no files that Editra can open in %s') % fname, _('No Valid Files to Open'), style=wx.OK | wx.CENTER | wx.ICON_INFORMATION)
                elif len(dcnt) > 5:
                    dlg = wx.MessageDialog(self, _('Do you wish to open all %d files in this directory?\n\nWarning: opening many files at once may cause the editor to temporarily  freeze.') % len(dcnt), _('Open Directory?'), style=wx.YES | wx.NO | wx.ICON_INFORMATION)
                if dlg is not None:
                    result = dlg.ShowModal()
                    dlg.Destroy()
                else:
                    result = wx.ID_YES
                if result == wx.ID_YES:
                    valid_files.extend(dcnt)
            else:
                valid_files.append(fname)

        for fname in valid_files:
            pathname = ebmlib.GetPathName(fname)
            the_file = ebmlib.GetFileName(fname)
            self.OpenPage(pathname, the_file)
            self.frame.PushStatusText(_('Opened file: %s') % fname, ed_glob.SB_INFO)

        return

    def OnIdle(self, evt):
        """Update tabs and check if files have been modified
        @param evt: wx.TimerEvent

        """
        if wx.GetApp().IsActive():
            for idx in range(self.GetPageCount()):
                page = self.GetPage(idx)
                if page is not None and page.IsShown():
                    page.DoOnIdle()

        return

    def OnPageChanging(self, evt):
        """Page changing event handler.
        @param evt: aui.EVT_AUINOTEBOOK_PAGE_CHANGING

        """
        evt.Skip()
        pages = (evt.GetOldSelection(), evt.GetSelection())
        self.LOG('[ed_pages][evt] Control Changing from Page: %d to Page: %d\n' % pages)
        if self.control:
            self.control.DoDeactivateTab()
        ed_msg.PostMessage(ed_msg.EDMSG_UI_NB_CHANGING, (
         self,) + pages, context=self.frame.Id)

    def ChangePage(self, pg_num, old=-2):
        """Change the page and focus to the the given page id
        @param pg_num: Page number to change
        @keyword old: previous selection

        """
        cpage = self.GetSelection()
        if cpage != pg_num:
            self.SetSelection(pg_num)
        window = self.GetPage(pg_num)
        self.control = window
        self.frame.SetTitle(self.control.GetTitleString())
        if old > -2:
            cpage = old
        if not self.frame.IsExiting() and cpage != pg_num:
            ed_msg.PostMessage(ed_msg.EDMSG_UI_NB_CHANGED, (
             self, pg_num), context=self.frame.Id)

    def OnPageChanged(self, evt):
        """Actions to do after a page change
        @param evt: aui.EVT_AUINOTEBOOK_PAGE_CHANGED

        """
        cpage = evt.GetSelection()
        self.ChangePage(cpage, old=evt.GetOldSelection())
        self.LOG('[ed_pages][evt] Page Changed to %d' % cpage)
        page = self.GetCurrentPage()
        if page:
            page.DoTabSelected()
        self.GoCurrentPage()

    def OnPageClosing(self, evt):
        """Checks page status to flag warnings before closing
        @param evt: aui.EVT_AUINOTEBOOK_PAGE_CLOSE

        """
        page = self.GetPage(evt.GetSelection())
        if page and page.CanCloseTab():
            sel = self.GetSelection()
            self.LOG('[ed_pages][evt] Closing Page: #%d' % sel)
            page.DoTabClosing()
            evt.Skip()
            ed_msg.PostMessage(ed_msg.EDMSG_UI_NB_CLOSING, (
             self, sel), context=self.frame.Id)
        else:
            evt.Veto()

    def OnPageClosed(self, evt):
        """Handles Paged Closed Event
        @param evt: aui.EVT_AUINOTEBOOK_PAGE_CLOSED

        """
        frame = self.TopLevelParent
        with eclib.Freezer(frame) as (_tmp):
            cpage = evt.GetSelection()
            evt.Skip()
            self.LOG('[ed_pages][evt] Closed Page: #%d' % cpage)
            self.UpdateIndexes()
            ed_msg.PostMessage(ed_msg.EDMSG_UI_NB_CLOSED, (
             self, cpage), context=self.frame.Id)
            if not self.GetPageCount() and hasattr(frame, 'IsExiting') and not frame.IsExiting():
                self.NewPage()
            elif not self.frame.IsExiting():
                self.SaveCurrentSession()

    def _ClosePageNum(self, idx, deletepg=True):
        """Close the given page
        @param idx: int
        @keyword deletepg: bool (Internal Use Only!)
        @return bool: was page deleted?

        """
        result = True
        try:
            page = self.GetPage(idx)
            result = page.CanCloseTab()
            if result and deletepg:
                evt = aui.AuiNotebookEvent(aui.wxEVT_COMMAND_AUINOTEBOOK_PAGE_CLOSE, SIMULATED_EVT_ID)
                evt.SetSelection(idx)
                self.OnPageClosing(evt)
                with eclib.Freezer(self.TopLevelParent) as (_tmp):
                    self.DeletePage(idx)
                evt = aui.AuiNotebookEvent(aui.wxEVT_COMMAND_AUINOTEBOOK_PAGE_CLOSED, SIMULATED_EVT_ID)
                evt.SetSelection(idx)
                self.OnPageClosed(evt)
        except Exception:
            pass

        return result

    def CloseAllPages(self):
        """Closes all open pages"""
        for page in range(self.GetPageCount()):
            if not self.ClosePage():
                break

    def CloseOtherPages(self):
        """Close all but the currently selected tab"""
        cpage = self.GetCurrentPage()
        to_del = list()
        for pnum in range(self.GetPageCount()):
            page = self.GetPage(pnum)
            if not page:
                break
            if not page == cpage:
                if page.CanCloseTab():
                    to_del.append(pnum)

        if len(to_del):
            to_del.sort()
            to_del.reverse()
            for pnum in to_del:
                self._ClosePageNum(pnum)

    def ClosePage(self, deletepg=True):
        """Closes currently selected page
        @keyword deletepg: bool (actually delete the page) internal use only
        @return: bool

        """
        pnum = self.GetSelection()
        result = self._ClosePageNum(pnum, deletepg)
        return result

    def CanClosePage(self):
        """Can the current page be closed?
        @return: bool

        """
        self.GoCurrentPage()
        page = self.GetCurrentPage()
        if page:
            return page.CanCloseTab()
        return False

    def UpdateAllImages(self):
        """Reload and Reset all images in the notebook pages and
        the corresponding imagelist to match those of the current theme
        @postcondition: all images in control are updated

        """
        bUseIcons = Profile_Get('TABICONS')
        for page in range(self.GetPageCount()):
            if bUseIcons:
                tab = self.GetPage(page)
                self.SetPageBitmap(page, tab.GetTabImage())
            else:
                self.SetPageBitmap(page, wx.NullBitmap)

        self.Refresh()

    def UpdateIndexes(self):
        """Update all page indexes"""
        pages = [ self.GetPage(page) for page in range(self.GetPageCount()) ]
        for (idx, page) in enumerate(pages):
            page.SetTabIndex(idx)

    def UpdatePageImage(self):
        """Updates the page tab image
        @postcondition: page image is updated to reflect any changes in ctrl

        """
        tab = self.GetCurrentPage()
        self.SetPageBitmap(self.GetSelection(), tab.GetTabImage())

    def OnUpdatePageText(self, evt):
        """Update the title text of the current page
        @param evt: stc.EVT_STC_MODIFY (unused)
        @note: this method must complete its work very fast it gets
               called every time a character is entered or removed from
               the document.

        """
        try:
            if self.control.Id == evt.Id:
                if self.control.IsLoading():
                    return
                pg_num = self.GetSelection()
                title = self.GetPageText(pg_num)
                if self.control.GetModify():
                    title = '*' + title
                if title != super(EdPages, self).GetPageText(pg_num):
                    self.SetPageText(pg_num, title)
                    ftitle = self.control.GetTitleString()
                    self.frame.SetTitle(ftitle)
            for page in range(self.GetPageCount()):
                control = self.GetPage(page)
                if control.Id == evt.Id:
                    title = self.GetPageText(page)
                    if control.GetModify():
                        title = '*' + title
                    if title != super(EdPages, self).GetPageText(page):
                        self.SetPageText(page, title)

        except wx.PyDeadObjectError:
            pass

    def UpdateTextControls(self):
        """Updates all text controls to use any new settings that have
        been changed since initialization.
        @postcondition: all stc controls in the notebook are reconfigured
                        to match profile settings

        """
        for control in self.GetTextControls():
            control.UpdateAllStyles()
            control.Configure()