# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_session.py
# Compiled at: 2012-03-17 12:57:55
"""
Editra session file manager.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_session.py 70097 2011-12-22 21:36:43Z CJP $'
__revision__ = '$Revision: 70097 $'
import wx, os, cPickle, util, ed_cmdbar, ed_glob, profiler, ed_msg, ebmlib
_ = wx.GetTranslation

class SessionManager(object):
    """Simple editing session manager helper class"""

    def __init__(self, savedir):
        """@param savedir: directory to load/save session files at"""
        super(SessionManager, self).__init__()
        self.__default = '__default'
        self._sessiondir = savedir
        self._sessionext = '.session'

    DefaultSession = property(lambda self: self.__default)
    SessionDir = property(lambda self: self._sessiondir, lambda self, dpath: setattr(self, '_sessiondir', dpath))

    def _SetExtension(self, ext):
        assert ext.startswith('.')
        self._sessionext = ext

    SessionExtension = property(lambda self: self._sessionext, lambda self, ext: self._SetExtension(ext))
    Sessions = property(lambda self: self.GetSavedSessions())

    def DeleteSession(self, name):
        """Delete the specified session name
        @param name: session name
        @return: bool

        """
        rval = True
        session = self.PathFromSessionName(name)
        if os.path.exists(session):
            try:
                os.remove(session)
            except OSError:
                rval = False

        return rval

    def GetSavedSessions(self):
        """Get the list of available saved sessions by display name
        @return: list of strings

        """
        sessions = list()
        defaultSession = None
        for session in os.listdir(self.SessionDir):
            if session.endswith(self.SessionExtension):
                path = os.path.join(self.SessionDir, session)
                sName = self.SessionNameFromPath(path)
                if session.startswith(self.__default):
                    defaultSession = sName
                else:
                    sessions.append(sName)

        sessions.sort()
        if defaultSession:
            sessions.insert(0, defaultSession)
        return sessions

    def LoadSession(self, name):
        """Load a named session
        @param name: session name
        @return: list of paths

        """
        session = self.PathFromSessionName(name)
        assert os.path.exists(session)
        flist = list()
        with open(session, 'rb') as (f_handle):
            try:
                flist = cPickle.load(f_handle)
                flist = flist.get('win1', list())
                for item in flist:
                    if type(item) not in (unicode, str):
                        raise TypeError('Invalid item in unpickled sequence')

            except (cPickle.UnpicklingError, TypeError, EOFError), e:
                util.Log('[ed_session][err] %s' % e)
                raise e

        return flist

    def SaveSession(self, name, paths):
        """Save the given list of files as a session with the given name
        @param name: session name
        @param paths: list of file paths
        @return: bool

        """
        session = self.PathFromSessionName(name)
        bOk = False
        with open(session, 'wb') as (f_handle):
            try:
                sdata = dict(win1=paths)
                cPickle.dump(sdata, f_handle)
                bOk = True
            except Exception, msg:
                util.Log('[ed_session][err] Failed to SaveSessionFile: %s' % msg)

        return bOk

    def PathFromSessionName(self, session):
        """Get the full path to store a session file
        @param session: string base name (no extension)

        """
        name = session + self.SessionExtension
        path = os.path.join(self.SessionDir, name)
        return path

    def SessionNameFromPath(self, path):
        """Get the sessions display name from its path"""
        assert path.endswith(self.SessionExtension)
        name = os.path.basename(path)
        name = name.rsplit('.', 1)[0]
        return name


class EdSessionMgr(SessionManager):
    """Editra specific session manager implementation"""
    __metaclass__ = ebmlib.Singleton

    def __init__(self):
        super(EdSessionMgr, self).__init__(ed_glob.CONFIG['SESSION_DIR'])


class EdSessionBar(ed_cmdbar.CommandBarBase):
    """Command bar for managing editing sessions"""

    class meta:
        id = ed_glob.ID_SESSION_BAR

    def __init__(self, parent):
        super(EdSessionBar, self).__init__(parent)
        self._sch = wx.Choice(self)
        self.__DoLayout()
        self._saveb = self.AddPlateButton(_('Save'), ed_glob.ID_SAVE)
        self._saveb.Name = 'SaveButton'
        self._saveasb = self.AddPlateButton(_('Save As'), ed_glob.ID_SAVEAS)
        self._saveasb.Name = 'SaveAsButton'
        self._delb = self.AddPlateButton(_('Delete'), ed_glob.ID_DELETE)
        self._delb.Name = 'DeleteButton'
        self.UpdateSessionList()
        self._saveb.Bind(wx.EVT_BUTTON, self.OnSaveSession)
        self._saveasb.Bind(wx.EVT_BUTTON, self.OnSaveSession)
        self._delb.Bind(wx.EVT_BUTTON, self.OnDeleteSession)
        self._sch.Bind(wx.EVT_CHOICE, self.OnChangeSession)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, self._delb)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        ed_msg.Subscribe(self.OnConfigMsg, ed_msg.EDMSG_PROFILE_CHANGE + ('LAST_SESSION', ))

    def __DoLayout(self):
        self.AddControl(wx.StaticText(self, label=_('Session:')), wx.ALIGN_LEFT)
        self.AddControl(self._sch, wx.ALIGN_LEFT)

    def OnDestroy(self, evt):
        """Cleanup message handlers"""
        if self:
            ed_msg.Unsubscribe(self.OnConfigMsg)
        evt.Skip()

    def GetSelectedSession(self):
        """Get the currently selected session
        @return: string (internal session name)

        """
        if self._sch.Selection == 0:
            return EdSessionMgr().DefaultSession
        else:
            return self._sch.StringSelection

    def OnChangeSession(self, evt):
        """Current session changed in choice control"""
        util.Log('[ed_session][info] OnChangeSession: %s' % self._sch.StringSelection)
        ed_msg.PostMessage(ed_msg.EDMSG_SESSION_DO_LOAD, self.GetSelectedSession(), self.TopLevelParent.Id)

    def OnConfigMsg(self, msg):
        """Configuration update callback"""
        if self:
            self.UpdateSessionList()

    def OnSaveSession(self, evt):
        """Save the current session"""
        ofiles = list()
        util.Log('[ed_session][info] OnSaveSession')
        if evt.EventObject is self._saveb:
            ed_msg.PostMessage(ed_msg.EDMSG_FILE_GET_OPENED, ofiles, self.TopLevelParent.Id)
            util.Log('[ed_session][info] OnSaveSession: %d files' % len(ofiles))
            EdSessionMgr().SaveSession(self.GetSelectedSession(), ofiles)
        elif evt.EventObject is self._saveasb:
            ed_msg.PostMessage(ed_msg.EDMSG_SESSION_DO_SAVE, context=self.TopLevelParent.Id)
        else:
            evt.Skip()

    def OnDeleteSession(self, evt):
        """Delete the current session"""
        if evt.EventObject is self._delb:
            ses = self.GetSelectedSession()
            if ses != EdSessionMgr().DefaultSession:
                EdSessionMgr().DeleteSession(ses)
                profiler.Profile_Set('LAST_SESSION', EdSessionMgr().DefaultSession)
        else:
            evt.Skip()

    def OnBarShown(self):
        """Update the session list"""
        self.UpdateSessionList()

    def OnUpdateUI(self, evt):
        """Handle UpdateUI events"""
        if evt.EventObject is self._delb:
            evt.Enable(self._sch.Selection > 0)
        else:
            evt.Skip()

    def UpdateSessionList(self):
        """Update the session list"""
        sessions = EdSessionMgr().Sessions
        if len(sessions):
            sessions[0] = _('Default')
            self._sch.Items = sessions
            self.UpdateSelectedSession()
            self.Layout()
            self.Refresh()

    def UpdateSelectedSession(self):
        """Select the currently configured session"""
        ses = profiler.Profile_Get('LAST_SESSION')
        if ses:
            if ses == EdSessionMgr().DefaultSession:
                self._sch.SetSelection(0)
            elif ses in self._sch.Items:
                self._sch.SetStringSelection(ses)