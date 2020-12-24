# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Pyreb\PyrebApp.py
# Compiled at: 2006-12-10 12:49:08
import wx, wx.xrc
from wx.xrc import XRCCTRL, XRCID
import Controls, Dialogs, sys, os.path, imp, pkg_resources
from Server import *
from exceptions import IOError
from optparse import OptionParser
PYREB_VERSION = '0.1.6'

class PyrebApp(wx.App):
    """
    Main Pyreb app.
    """
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        self.PYREB_VERSION = PYREB_VERSION
        self.XMLRPCServer = None
        if self.IsFrozen():
            self.BaseDir = sys.executable
            while not os.path.isdir(self.BaseDir):
                self.BaseDir = os.path.split(self.BaseDir)[0]

        wx.App.__init__(self, args, kwargs)
        return

    def IsFrozen(self):
        return hasattr(sys, 'frozen') or hasattr(sys, 'importers') or imp.is_frozen('__main__')

    def OnSetText(self, event):
        t = self.dialog['ID_TEXT']
        self.dialog['ID_TEXT'] = event.text
        event.text = t

    def OnGetText(self, event):
        event.text = self.dialog['ID_TEXT']

    def OnSetRegex(self, event):
        t = self.dialog['ID_REGEX']
        self.dialog['ID_REGEX'] = event.text
        event.text = t

    def OnGetRegex(self, event):
        event.text = self.dialog['ID_REGEX']

    def OnExit(self):
        if self.XMLRPCServer:
            self.XMLRPCServer.Mutex.release()
            self.XMLRPCServer.join(1.0)

    def GetResourceAsString(self, Name):
        Res = ''
        if self.IsFrozen():
            ResourceFile = os.path.join(self.BaseDir, 'Resource', Name)
            fd = file(ResourceFile, 'r')
            Res = fd.read()
            del fd
        else:
            try:
                Res = pkg_resources.resource_string('Pyreb', 'Resource/%s' % Name)
            except:
                raise IOError("Can't find the resource file %s. Pyreb installation is corrupt." % Name)

        return Res

    def OnInit(self):
        """
        Find the resource file, load the GUI and start the application.
        """
        if not self.CheckWxVersion(2, 6, 0):
            return False
        try:
            self.ResourceAsString = self.GetResourceAsString('pyreb_wxglade.xrc')
        except IOError, msg:
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
            sys.exit(1)

        self.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)
        assert self.ResourceAsString != ''
        self.Resource = wx.xrc.EmptyXmlResource()
        self.Resource.InsertHandler(Controls.PyrebResultsTreeXmlHandler())
        self.Resource.InsertHandler(Controls.PyrebRegexCtrlXmlHandler())
        self.Resource.LoadFromString(self.ResourceAsString)
        del self.ResourceAsString
        self.dialog = self.Resource.LoadFrame(None, 'MAIN')
        assert self.dialog is not None, 'Cannot load main application frame'
        self.dialog.SetTitle('Pyreb v. %s / wxWidgets %s' % (PYREB_VERSION, wx.VERSION_STRING))
        self.SetTopWindow(self.dialog)
        self.dialog.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.dialog.SetStatusText('Ready')
        self.dialog.SetStatusText('XMLRPC Server not running', 1)
        parser = OptionParser()
        parser.set_defaults(startServer=False, serverPort=17787)
        parser.add_option('-s', '--server', dest='startServer', action='store_true', help='Launch XMLRPC server at startup. Default: No')
        parser.add_option('-p', '--port', dest='serverPort', action='store', type='int', help='Port to which the XMLRPC server is bound. Default: 17787')
        (options, args) = parser.parse_args()
        self.serverPort = int(options.serverPort)
        if options.startServer:
            self.StartXMLRPCServer()
        self.dialog.Show()
        self.Bind(EVT_EXT_SETTEXT, self.OnSetText)
        self.Bind(EVT_EXT_GETTEXT, self.OnGetText)
        self.Bind(EVT_EXT_SETREGEX, self.OnSetRegex)
        self.Bind(EVT_EXT_GETREGEX, self.OnGetRegex)
        self.Bind(wx.EVT_MENU, self.OnStartXMLRPCServer, id=XRCID('ID_STARTSERVER'))
        return True

    def OnStartXMLRPCServer(self, event):
        if self.XMLRPCServer:
            wx.MessageBox('Server should be already running.', 'Error')
            return
        dlg = self.Resource.LoadDialog(self.dialog, 'PORTINPUT')
        dlg.ShowModal()
        self.serverPort = dlg.Port
        self.StartXMLRPCServer()

    def StartXMLRPCServer(self):
        if self.XMLRPCServer:
            return
        self.XMLRPCServer = PyrebXMLRPCServer(self.dialog, self.serverPort)
        self.XMLRPCServer.Mutex.acquire()
        self.XMLRPCServer.setDaemon(True)
        self.XMLRPCServer.start()
        Menu = self.dialog.GetMenuBar()
        assert Menu
        Menu.Enable(XRCID('ID_STARTSERVER'), False)
        self.dialog.SetStatusText('XMLRPC Server running on localhost:%s' % self.serverPort, 1)
        wx.MessageBox('Server started OK')

    def OnQuitServer(self, event):
        print 'OnQuitServer'

    def CheckWxVersion(self, Major, Minor, Micro):
        (wxMaj, wxMin, wxMic, wxRes, s) = wx.VERSION
        Req = Major * 100 + Minor * 10 + Micro
        Got = wxMaj * 100 + wxMin * 10 + wxMic
        if Req > Got:
            msg = 'Pyreb requires at least wxWidgets %d.%d.%d, you have %d.%d.%d' % (Major, Minor, Micro, wxMaj, wxMin, wxMic)
            wx.MessageBox(msg, 'wxWidgets version check failed', wx.OK | wx.ICON_ERROR)
            return False
        return True


def main():
    app = PyrebApp(redirect=True)
    app.MainLoop()


if __name__ == '__main__':
    main()