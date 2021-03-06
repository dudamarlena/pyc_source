# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hgwin\taskbaricon.py
# Compiled at: 2007-12-29 00:20:11
import wx, sys, servers

class HGWIN_TASKBARICON(wx.TaskBarIcon):
    ID_EXIT = 1
    ID_NEW_CONNECTION = 2
    ID_DELETE = 10000
    ID_EDIT = 20000
    ID_STARTSTOP = 30000
    ID_COPY = 40000

    def __init__(self):
        wx.TaskBarIcon.__init__(self)
        self.Bind(wx.EVT_MENU, self.OnExitClicked, id=self.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnNewConnectionClicked, id=self.ID_NEW_CONNECTION)
        self.Caption = ''

    def SetIcon(self, filename):
        bmp = wx.Bitmap(filename)
        self.Icon = wx.EmptyIcon()
        self.Icon.CopyFromBitmap(bmp)
        wx.TaskBarIcon.SetIcon(self, self.Icon, self.Caption)

    def SetCaption(self, caption):
        self.Caption = caption
        self.SetIcon(self.Icon, self.Caption)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_NEW_CONNECTION, 'New Server')
        menu.AppendSeparator()
        for (i, reposerver) in enumerate(servers.GetServer()):
            subMenu = wx.Menu()
            if reposerver.IsServing():
                subMenu.Append(self.ID_STARTSTOP + i, 'Stop')
            else:
                subMenu.Append(self.ID_STARTSTOP + i, 'Start')
            subMenu.Append(self.ID_EDIT + i, 'Edit')
            subMenu.Append(self.ID_DELETE + i, 'Delete')
            subMenu.AppendSeparator()
            subMenu.Append(self.ID_COPY + i, 'Copy URL to Clipboard')
            menu.AppendMenu(-1, '%s port %d' % (reposerver.Name, reposerver.Port), subMenu)
            self.Bind(wx.EVT_MENU, self.OnStartStopClicked, id=self.ID_STARTSTOP + i)
            self.Bind(wx.EVT_MENU, self.OnEditClicked, id=self.ID_EDIT + i)
            self.Bind(wx.EVT_MENU, self.OnDeleteClicked, id=self.ID_DELETE + i)
            self.Bind(wx.EVT_MENU, self.OnCopyClicked, id=self.ID_COPY + i)

        menu.AppendSeparator()
        menu.Append(self.ID_EXIT, 'Exit')
        return menu

    def OnExitClicked(self, event):
        servers.SaveServers('serverlist.py')
        wx.Exit()

    def OnNewConnectionClicked(self, event):
        import newconnectiondialog
        dlg = newconnectiondialog.HGWIN_NEW_CONNECTION_DIALOG(None, -1, 'Create a New Repository Server')
        dlg.ShowModal()
        dlg.Destroy()
        return

    def OnStartStopClicked(self, event):
        serverIndex = event.GetId() - self.ID_STARTSTOP
        server = servers.GetServerByIndex(serverIndex)
        print str(server)
        if server.IsServing():
            server.StopServing()
        else:
            server.StartServing()

    def OnEditClicked(self, event):
        import newconnectiondialog
        serverIndex = event.GetId() - self.ID_EDIT
        server = servers.GetServerByIndex(serverIndex)
        if server.IsServing():
            res = wx.MessageBox('This server is currently running.  The server will be stopped if you decide to edit its properties.  Continue?', 'Question', wx.YES_NO | wx.CENTRE | wx.NO_DEFAULT, None)
            if res == wx.NO:
                return
            server.StopServing()
        dlg = newconnectiondialog.HGWIN_NEW_CONNECTION_DIALOG(None, -1, 'Create a New Repository Server')
        dlg.SetTitle('Edit a Repository Server')
        dlg.Edit(server)
        dlg.ShowModal()
        dlg.Destroy()
        return

    def OnDeleteClicked(self, event):
        serverIndex = event.GetId() - self.ID_DELETE
        server = servers.GetServerByIndex(serverIndex)
        servers.RemoveServerByName(server.Name)

    def OnCopyClicked(self, event):
        import socket
        serverIndex = event.GetId() - self.ID_COPY
        server = servers.GetServerByIndex(serverIndex)
        urlstring = 'http://%s:%d/hg' % (socket.gethostname(), server.Port)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(urlstring))
            wx.TheClipboard.Close()