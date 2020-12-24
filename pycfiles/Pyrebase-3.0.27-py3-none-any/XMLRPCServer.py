# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Pyreb\Server\XMLRPCServer.py
# Compiled at: 2006-12-10 11:46:53
import threading, SimpleXMLRPCServer, wx
myEVT_EXT_SETTEXT = wx.NewEventType()
EVT_EXT_SETTEXT = wx.PyEventBinder(myEVT_EXT_SETTEXT)
myEVT_EXT_GETTEXT = wx.NewEventType()
EVT_EXT_GETTEXT = wx.PyEventBinder(myEVT_EXT_GETTEXT)
myEVT_EXT_SETREGEX = wx.NewEventType()
EVT_EXT_SETREGEX = wx.PyEventBinder(myEVT_EXT_SETREGEX)
myEVT_EXT_GETREGEX = wx.NewEventType()
EVT_EXT_GETREGEX = wx.PyEventBinder(myEVT_EXT_GETREGEX)
myEVT_EXT_QUIT = wx.NewEventType()
EVT_EXT_QUIT = wx.PyEventBinder(myEVT_EXT_QUIT)

class SetTextEvent(wx.PyEvent):
    """
    Custom wxPython event, needed to communicate a "Set" action
    to pyreb.
    """
    __module__ = __name__

    def __init__(self, evtType, txt):
        wx.PyEvent.__init__(self, eventType=evtType)
        self.text = txt


class GetTextEvent(wx.PyEvent):
    """
    Custom wxPython event, needed to communicate a "Get" action
    to pyreb.
    """
    __module__ = __name__

    def __init__(self, evtType):
        wx.PyEvent.__init__(self, eventType=evtType)
        self.text = ''


class QuitEvent(wx.PyEvent):
    """
    Custom wxPython event; quits XML-RPC server upon reception.
    """
    __module__ = __name__

    def __init__(self):
        wx.PyEvent.__init__(self, eventType=EVT_EXT_QUIT)


class PyrebAPI:
    """
    Methods exported by the XMLRPC server.
    """
    __module__ = __name__

    def __init__(self, Wnd):
        """
        Initializes the API container
        @param Wnd: Pyreb main window, needed to pass events along
        """
        assert isinstance(Wnd, wx.Window)
        self.Wnd = Wnd

    def setText(self, Text):
        """
        Set the text in the 'Text to analyze' control. The actual regex will
        be appliead against the new text.
        @param Text: Text to be displayed
        @return: Previous text in the control
        """
        evt = SetTextEvent(myEVT_EXT_SETTEXT, Text)
        self.Wnd.GetEventHandler().ProcessEvent(evt)
        return evt.text

    def getText(self):
        """
        Get the text in the 'Text to analyze' control
        @return: Text in the control
        """
        evt = GetTextEvent(myEVT_EXT_GETTEXT)
        self.Wnd.GetEventHandler().ProcessEvent(evt)
        return evt.text

    def setRegex(self, Text):
        """
        Set the Regular expression. After being set, the regex will be applied
        @param Text: Regex to be set and applied
        @return: Previous text in the control
        """
        evt = SetTextEvent(myEVT_EXT_SETREGEX, Text)
        self.Wnd.GetEventHandler().ProcessEvent(evt)
        return evt.text

    def getRegex(self):
        """
        Get the Regular expression.
        @return: Current regex.
        """
        evt = GetTextEvent(myEVT_EXT_GETREGEX)
        self.Wnd.GetEventHandler().ProcessEvent(evt)
        return evt.text

    def Quit(self):
        print 'QuitEvent'
        evt = QuitEvent()
        self.Wnd.GetEventHandler().ProcessEvent(evt)


def handlerSetup(handler, API):
    handler.register_introspection_functions()
    handler.register_function(API.setText, 'Pyreb.setText')
    handler.register_function(API.getText, 'Pyreb.getText')
    handler.register_function(API.setRegex, 'Pyreb.setRegex')
    handler.register_function(API.getRegex, 'Pyreb.getRegex')


class PyrebXMLRPCServer(threading.Thread):
    """
    Simple XMLRPC server to control Pyreb instance.
    The server is run in a separate thread. The pyreb instance
    is controlled using custom wxWidgets events: for this reason
    the server needs pyreb main window instance.
    """
    __module__ = __name__

    def __init__(self, Wnd, Port=17787):
        """
        Initialize the server.
        @param Wnd: Pyreb main window
        @param Port: Port to bind the server
        """
        threading.Thread.__init__(self)
        self.Port = Port
        self.Wnd = Wnd
        self.Mutex = threading.Lock()

    def run(self):
        handler = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', self.Port), logRequests=False)
        api = PyrebAPI(self.Wnd)
        handlerSetup(handler, api)
        while True:
            if True == self.Mutex.acquire(0):
                return
            handler.handle_request()