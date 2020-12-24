# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hgwin\hgwin.py
# Compiled at: 2007-12-29 00:20:11
import wx
from taskbaricon import *
import servers, os.path
Version = '1.0'

class TaskBarApp(wx.Frame):

    def __init__(self, parent, id, title):
        pass


class HGWIN_APPLICATION(wx.App):

    def OnInit(self):
        self.TaskBarIcon = HGWIN_TASKBARICON()
        self.TaskBarIcon.SetIcon(os.path.join(os.path.dirname(__file__), 'icon.bmp'))
        return True


def main():
    servers.LoadServers('serverlist.py')
    app = HGWIN_APPLICATION(0)
    app.MainLoop()


if __name__ == '__main__':
    main()