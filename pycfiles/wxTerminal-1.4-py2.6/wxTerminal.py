# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wxTerminal/wxTerminal.py
# Compiled at: 2013-01-31 10:43:47
try:
    import wx
except ImportError:
    print 'wxTerminal requires wxPython which is missing from your system'
    print 'wxPython currently does not use distutils so is not automatically installed'
    print 'you can install wxPython by visiting http://www.wxpython.org'
    raise

import wxSerialConfigDialog, serial, threading, argparse, logging, sys, csFIFO, SocketServer
from Singleton import Singleton
import time, socket
from multiprocessing import queues
from wxTerminalMP import *
LOGLEVEL = logging.ERROR
log = logging.getLogger(__package__)
log.setLevel(LOGLEVEL)
con = logging.StreamHandler()
con.setLevel(LOGLEVEL)
log.addHandler(con)

def fixLF(text, find, replace):
    """Repeatidly replace find with replace until there are no more instances
        e.g. fixLF(a,"

","
")
        will replace multiple 

 with a single one"""
    while True:
        t = text.replace(find, replace)
        if text == t:
            break
        print t
        print text
        text = t

    return text


def makePrint(string):
    """Replace non-printable characters with their hex number"""
    return ('').join([ c if ord(c) > 31 and ord(c) < 127 else '<%02X>' % ord(c) for c in string ])


SERIALRX = wx.NewEventType()
APPMSG = wx.NewEventType()
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 1)
EVT_APPMSG = wx.PyEventBinder(APPMSG, 1)

class SerialRxEvent(wx.PyCommandEvent):
    eventType = SERIALRX

    def __init__(self, windowID, data):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)


class AppMsgEvent(wx.PyCommandEvent):
    eventType = APPMSG

    def __init__(self, windowID, data):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)


ID_CLEAR = wx.NewId()
ID_SAVEAS = wx.NewId()
ID_SETTINGS = wx.NewId()
ID_TERM = wx.NewId()
ID_EXIT = wx.NewId()
NEWLINE_NONE = 0
NEWLINE_CR = 1
NEWLINE_LF = 2
NEWLINE_CRLF = 3
NEWLINE_LFCR = 4
NEWLINES = {'NONE': NEWLINE_NONE, 'CR': NEWLINE_CR, 'LF': NEWLINE_LF, 'CRLF': NEWLINE_CRLF, 'LFCR': NEWLINE_LFCR}
PARITIES = (
 'None', 'Odd', 'Even', 'Mark', 'Space')
DEF_SSPORT = 56712
DEF_BAUD = 115200
DEF_STOP = 1
DEF_PARITY = 'None'
DEF_BITS = 8
DEF_TIMEOUT = 0.1
DEF_SP_NEWLINE = 'NONE'
DEF_KB_NEWLINE = 'CR'
DEF_SETTINGS = {'port': None, 
   'baudrate': DEF_BAUD, 
   'bytesize': DEF_BITS, 
   'parity': DEF_PARITY, 
   'stopbits': DEF_STOP, 
   'rtscts': False, 
   'xonxoff': False, 
   'timeout': DEF_TIMEOUT, 
   'echo': False, 
   'unprintable': False, 
   'sp_newline': DEF_SP_NEWLINE, 
   'kb_newline': DEF_KB_NEWLINE, 
   'lockKB': False, 
   'snoopserver': False, 
   'D': False}

def ScanBackspace(text):
    scantext = text
    start = 0
    done = False
    for c in text:
        if c == chr(8):
            start = start + 1
        else:
            break

    while not done:
        done = True
        pos = scantext[start:].find(chr(8))
        if pos > 0:
            scantext = scantext[start:][:pos - 1] + scantext[start:][pos + 1:]
            done = False

    return text[0:start] + scantext


class TerminalSetup(object):
    """Placeholder for various terminal settings. Used to pass the
           options to the TerminalSettingsDialog."""

    def __init__(self, PortSettings):
        [ self.__setattr__(k, DEF_SETTINGS[k]) for k in DEF_SETTINGS.keys() ]
        [ self.__setattr__(k, PortSettings[k]) for k in PortSettings.keys() ]

    def __str__(self):
        return str(self.__dict__)


class TerminalSettingsDialog(wx.Dialog):
    """Simple dialog with common terminal settings like echo, newline mode."""

    def __init__(self, *args, **kwds):
        self.settings = kwds['settings']
        del kwds['settings']
        kwds['style'] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.checkbox_echo = wx.CheckBox(self, -1, 'Local Echo')
        self.checkbox_unprintable = wx.CheckBox(self, -1, 'Show unprintable characters')
        self.radio_box_newline = wx.RadioBox(self, -1, 'Newline Handling', choices=['None', 'CR only', 'LF only', 'CR+LF'], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
        self.button_ok = wx.Button(self, -1, 'OK')
        self.button_cancel = wx.Button(self, -1, 'Cancel')
        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.checkbox_echo.SetValue(self.settings.echo)
        self.checkbox_unprintable.SetValue(self.settings.unprintable)
        self.radio_box_newline.SetSelection(self.settings.newline)

    def __set_properties(self):
        self.SetTitle('Terminal Settings')
        self.radio_box_newline.SetSelection(0)
        self.button_ok.SetDefault()

    def __do_layout(self):
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Input/Output'), wx.VERTICAL)
        sizer_4.Add(self.checkbox_echo, 0, wx.ALL, 4)
        sizer_4.Add(self.checkbox_unprintable, 0, wx.ALL, 4)
        sizer_4.Add(self.radio_box_newline, 0, 0, 0)
        sizer_2.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_3.Add(self.button_ok, 0, 0, 0)
        sizer_3.Add(self.button_cancel, 0, 0, 0)
        sizer_2.Add(sizer_3, 0, wx.ALL | wx.ALIGN_RIGHT, 4)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        sizer_2.SetSizeHints(self)
        self.Layout()

    def __attach_events(self):
        self.Bind(EVT_BUTTON, self.OnOK, id=self.button_ok.GetId())
        self.Bind(EVT_BUTTON, self.OnCancel, id=self.button_cancel.GetId())

    def OnOK(self, events):
        """Update data wil new values and close dialog."""
        self.settings.echo = self.checkbox_echo.GetValue()
        self.settings.unprintable = self.checkbox_unprintable.GetValue()
        self.settings.newline = self.radio_box_newline.GetSelection()
        self.EndModal(wx.ID_OK)

    def OnCancel(self, events):
        """Do not update data but close dialog."""
        self.EndModal(wx.ID_CANCEL)


@Singleton
class AllClients(dict):

    def __init__(self, *args, **kw):
        if not hasattr(self, 'lock'):
            self.lock = threading.Lock()
            self.S2C = csFIFO.FIFO(max_size=10000000.0)
            self.C2S = csFIFO.FIFO(max_size=10000000.0)
            self.IsActive = True
            self.writeThread = threading.Thread(target=self.writer)
            self.writeThread.setDaemon(1)
            self.writeThread.start()
        super(AllClients, self).__init__(*args, **kw)

    def write(self, data):
        """Write data to all clients"""
        self.S2C.write(data)

    def read(self, size):
        """Read data written by all clients"""
        return self.C2S.read(size)

    def inWaiting(self):
        return not self.C2S.isEmpty()

    def destroy(self):
        self.IsActive = False
        self.writeThread.join()

    def writer(self):
        while self.IsActive:
            if not self.S2C.isEmpty():
                data = self.S2C.read(-1)
                self.lock.acquire()
                for (name, client) in self.iteritems():
                    if isinstance(client, SerialTCPHandler) and client.IsActive:
                        try:
                            client.wfile.write(data)
                        except socket.error, er:
                            client.IsActive = False

                self.lock.release()
            else:
                time.sleep(0.1)

        print 'Writer exit'
        print self.IsActive

    def addClient(self, client):
        print 'Adding client %s' % repr(client.client_address)
        self.lock.acquire()
        self[repr(client.client_address)] = client
        self.lock.release()

    def delClient(self, client):
        self.lock.acquire()
        try:
            self.pop(repr(client.client_address))
            print 'Removed client %s' % repr(client.client_address)
        except KeyError:
            pass

        self.close(client)
        self.lock.release()

    def close(self, client):
        try:
            if not client.wfile.closed:
                client.wfile.flush()
                client.wfile.close()
        except socket.error:
            pass

        client.rfile.close()

    def closeAll(self):
        for (name, client) in self.iteritems():
            print 'Closing %s' % name
            self.close(client)


class SerialTCPHandler(SocketServer.StreamRequestHandler):

    def __init__(self, *args, **kw):
        self.IsActive = True
        self.clients = AllClients()
        SocketServer.StreamRequestHandler.__init__(self, *args, **kw)
        self.timeout = 0.1

    def handle(self):
        while self.IsActive and not self.rfile.closed:
            try:
                data = self.rfile.readline()
            except socket.error, er:
                print er
            else:
                self.clients.C2S.write(data)

        print '%s Disconnected' % repr(self.client_address)

    def setup(self):
        self.clients.addClient(self)
        return SocketServer.StreamRequestHandler.setup(self)

    def finish(self, *args, **kw):
        self.clients.delClient(self)


class SerialTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, handler_class=SerialTCPHandler):
        self.clients = AllClients()
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        print 'Server on %s' % str(server_address)

    def write(self, data):
        self.clients.write(data)

    def read(self, size):
        return self.clients.read(size)


class TerminalFrame(wx.Frame):
    """Simple terminal program for wxPython"""

    def __init__(self, *args, **kwds):
        global log
        self.serial = None
        self.SerialThread = None
        self.AppMsgThread = None
        self.SerialAlive = None
        self.AppMsgAlive = None
        self.server = None
        self.clients = AllClients()
        self.logoutbuffer = []
        self.loginbuffer = []
        self.keysLock = threading.Lock()
        self.log = log
        kwds['style'] = wx.DEFAULT_FRAME_STYLE
        if kwds.has_key('PortSettings'):
            PortSettings = kwds['PortSettings']
            del kwds['PortSettings']
        else:
            PortSettings = {}
        if kwds.has_key('AppMsgQueue'):
            self.AppMsgQueue = kwds['AppMsgQueue']
            del kwds['AppMsgQueue']
        else:
            self.AppMsgQueue = None
        self.settings = TerminalSetup(PortSettings)
        if hasattr(self.settings, 'D'):
            if self.settings.D:
                self.log.setLevel(logging.DEBUG)
            self.log.debug(self.settings)
            if isinstance(self.settings.kb_newline, str):
                self.settings.kb_newline = NEWLINES[self.settings.kb_newline]
            if isinstance(self.settings.sp_newline, str):
                self.settings.sp_newline = NEWLINES[self.settings.sp_newline]
            wx.Frame.__init__(self, *args, **kwds)
            self.text_ctrl_output = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
            textFont = wx.Font(8, wx.TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            textStyle = wx.TextAttr()
            textStyle.SetFont(textFont)
            self.text_ctrl_output.SetDefaultStyle(textStyle)
            self.frame_terminal_menubar = wx.MenuBar()
            self.SetMenuBar(self.frame_terminal_menubar)
            wx.glade_tmp_menu = wx.Menu()
            wx.glade_tmp_menu.Append(ID_CLEAR, '&Clear', '', wx.ITEM_NORMAL)
            wx.glade_tmp_menu.Append(ID_SAVEAS, '&Save Text As...', '', wx.ITEM_NORMAL)
            wx.glade_tmp_menu.AppendSeparator()
            wx.glade_tmp_menu.Append(ID_SETTINGS, '&Port Settings...', '', wx.ITEM_NORMAL)
            wx.glade_tmp_menu.Append(ID_TERM, '&Terminal Settings...', '', wx.ITEM_NORMAL)
            wx.glade_tmp_menu.AppendSeparator()
            wx.glade_tmp_menu.Append(ID_EXIT, '&Exit', '', wx.ITEM_NORMAL)
            self.frame_terminal_menubar.Append(wx.glade_tmp_menu, '&File')
            self.__set_properties()
            self.__do_layout()
            if self.AppMsgQueue:
                self.AppMsgAlive = threading.Event()
                self.StartAppMsgThread()
            if len(PortSettings) == 0:
                log.debug('No parameters passed, use settings dialog')
                self.OnPortSettings(None)
            print PortSettings.has_key('port') or 'port parameter is mandatory'
        else:
            self.serial = serial.serial_for_url(url=PortSettings['port'], do_not_open=True)
            self.serial.setTimeout(0.1)
            self.SerialAlive = threading.Event()
            if PortSettings.has_key('baudrate'):
                self.serial.setBaudrate(PortSettings['baudrate'])
            if PortSettings.has_key('bytesize'):
                self.serial.setByteSize(PortSettings['bytesize'])
            if PortSettings.has_key('stopbits'):
                self.serial.setStopbits(PortSettings['stopbits'])
            if PortSettings.has_key('parity'):
                self.serial.setParity(PortSettings['parity'][0])
            if PortSettings.has_key('rtscts'):
                self.serial.setRtsCts(PortSettings['rtscts'])
            if PortSettings.has_key('xonxoff'):
                self.serial.setXonXoff(PortSettings['xonxoff'])
            if PortSettings.has_key('timeout'):
                self.serial.setTimeout(PortSettings['timeout'])
            if PortSettings.has_key('snoopserver'):
                if PortSettings['snoopserver']:
                    if isinstance(PortSettings['snoopserver'], int):
                        self.ssport = PortSettings['snoopserver']
                    else:
                        self.ssport = DEF_SSPORT
                    self.EnableBackdoor()
            log.debug('Opening port %s' % self.serial.getPort())
            try:
                self.serial.open()
                self.serial.setRTS(0)
                self.serial.setDTR(0)
            except serial.SerialException, e:
                dlg = wx.MessageDialog(None, str(e), 'Serial Port Error', wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                self.StartThread()
                self.SetTitle('Serial Terminal on %s [%s, %s%s%s%s%s]' % (
                 self.serial.portstr,
                 self.serial.baudrate,
                 self.serial.bytesize,
                 self.serial.parity,
                 self.serial.stopbits,
                 self.serial.rtscts and ' RTS/CTS' or '',
                 self.serial.xonxoff and ' Xon/Xoff' or ''))

            self.__attach_events()
            if not self.SerialAlive.isSet():
                self.Close()
            if self.AppMsgQueue and not self.AppMsgAlive.isSet():
                self.Close()
            return

    def EnableBackdoor(self):
        self.server = SerialTCPServer(('localhost', self.ssport))
        t = threading.Thread(target=self.server.serve_forever)
        t.daemon = True
        t.start()

    def StartThread(self):
        """Start the receiver thread"""
        log.debug('Starting serial thread')
        self.SerialThread = threading.Thread(target=self.SerialThreadFunc)
        self.SerialThread.daemon = True
        self.SerialAlive.set()
        self.SerialThread.start()

    def StartAppMsgThread(self):
        """Start the receiver thread"""
        log.debug('Starting AppMsg thread')
        self.AppMsgThread = threading.Thread(target=self.AppMsgThreadFunc)
        self.AppMsgThread.daemon = True
        self.AppMsgAlive.set()
        self.AppMsgThread.start()

    def StopThreads(self):
        """Stop the receiver thread, wait util it's finished."""
        if self.AppMsgThread:
            self.AppMsgAlive.clear()
            self.AppMsgThread.join()
            self.AppMsgThread = None
        if self.SerialThread:
            self.SerialAlive.clear()
            self.SerialThread.join()
            self.SerialThread = None
        if self.server is not None:
            print 'Disconnecting clients'
            self.clients.closeAll()
            print 'Closing server'
            self.server.shutdown()
            self.server = None
        return

    def __set_properties(self):
        self.SetTitle('Serial Terminal')
        self.SetSize((800, 600))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.text_ctrl_output, 1, wx.EXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        self.Layout()

    def __attach_events(self):
        self.Bind(wx.EVT_MENU, self.OnClear, id=ID_CLEAR)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id=ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnPortSettings, id=ID_SETTINGS)
        self.Bind(wx.EVT_MENU, self.OnTermSettings, id=ID_TERM)
        self.text_ctrl_output.Bind(wx.EVT_CHAR, self.OnKey)
        self.Bind(EVT_SERIALRX, self.OnSerialRead)
        self.Bind(EVT_APPMSG, self.OnAppMsg)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnExit(self, event):
        """Menu point Exit"""
        self.Close()

    def OnClose(self, event):
        """Called on application shutdown."""
        self.StopThreads()
        self.serial.close()
        self.Destroy()

    def OnSaveAs(self, event):
        """Save contents of output window."""
        filename = None
        dlg = wx.FileDialog(None, 'Save Text As...', '.', '', 'Text File|*.txt|All Files|*', wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
        dlg.Destroy()
        if filename is not None:
            f = file(filename, 'w')
            text = self.text_ctrl_output.GetValue()
            if type(text) == unicode:
                text = text.encode('latin1')
            f.write(text)
            f.close()
        return

    def OnClear(self, event):
        """Clear contents of output window."""
        self.text_ctrl_output.Clear()

    def OnPortSettings(self, event=None):
        """Show the portsettings dialog. The reader thread is stopped for the
                   settings change."""
        if event is not None:
            self.StopThreads()
            self.serial.close()
        ok = False
        while not ok:
            dialog_serial_cfg = wxSerialConfigDialog.SerialConfigDialog(None, -1, '', show=wxSerialConfigDialog.SHOW_BAUDRATE | wxSerialConfigDialog.SHOW_FORMAT | wxSerialConfigDialog.SHOW_FLOW, serial=self.serial)
            result = dialog_serial_cfg.ShowModal()
            dialog_serial_cfg.Destroy()
            if result == wx.ID_OK or event is not None:
                try:
                    self.serial.open()
                    self.serial.setRTS(0)
                    self.serial.setDTR(0)
                except serial.SerialException, e:
                    dlg = wx.MessageDialog(None, str(e), 'Serial Port Error', wx.OK | wx.ICON_ERROR)
                    dlg.ShowModal()
                    dlg.Destroy()
                else:
                    self.StartThread()
                    self.SetTitle('Serial Terminal on %s [%s, %s%s%s%s%s]' % (
                     self.serial.portstr,
                     self.serial.baudrate,
                     self.serial.bytesize,
                     self.serial.parity,
                     self.serial.stopbits,
                     self.serial.rtscts and ' RTS/CTS' or '',
                     self.serial.xonxoff and ' Xon/Xoff' or ''))
                    ok = True
            else:
                self.alive.clear()
                ok = True

        return

    def OnTermSettings(self, event):
        """Menu point Terminal Settings. Show the settings dialog
                   with the current terminal settings"""
        dialog = TerminalSettingsDialog(None, -1, '', settings=self.settings)
        result = dialog.ShowModal()
        dialog.Destroy()
        return

    def handleKeys(self, chars):
        if isinstance(chars, (list, tuple, str)):
            for c in chars:
                code = ord(c)
                if code == 13 or code == 10:
                    if self.settings.echo:
                        self.text_ctrl_output.AppendText('\n')
                    if self.settings.kb_newline == NEWLINE_NONE:
                        char = c
                    elif self.settings.kb_newline == NEWLINE_CR:
                        char = '\r'
                    elif self.settings.kb_newline == NEWLINE_LF:
                        char = '\n'
                    elif self.settings.kb_newline == NEWLINE_CRLF:
                        char = '\r\n'
                    elif self.settings.kb_newline == NEWLINE_LFCR:
                        char = '\n\r'
                    self.logoutbuffer.append(char)
                    s = ('').join(self.logoutbuffer)
                    self.logoutbuffer = []
                    log.debug(':> %s' % makePrint(s))
                else:
                    char = c
                    self.logoutbuffer.append(char)
                    if self.settings.echo:
                        if code == 8:
                            self.text_ctrl_output.SetEditable(1)
                            curpos = self.text_ctrl_output.GetLastPosition()
                            self.text_ctrl_output.Remove(curpos - 1, curpos)
                            self.text_ctrl_output.SetEditable(0)
                            self.text_ctrl_output.SendTextUpdatedEvent()
                        else:
                            self.text_ctrl_output.WriteText(char)
                self.serial.write(char)

    def OnKey(self, event):
        """Key event handler. if the key is in the ASCII range, write it to the serial port.
                   Newline handling and local echo is also done here."""
        if not hasattr(self.settings, 'lockKB') or not self.settings.lockKB:
            code = event.GetKeyCode()
            if code < 256:
                char = chr(code)
                self.handleKeys(char)
            else:
                log.debug('CODE: %d' % code)
                print 'Extra Key:', code

    def OnAppMsg(self, event):
        try:
            (msgtype, data) = event.data
        except Exception:
            msgtype = None

        if msgtype == wxtMsg.AM_QUIT and data == 'QUIT!':
            self.Close()
        elif msgtype == wxtMsg.AM_DIALOG:
            dlg = wx.MessageDialog(None, str(data), 'wxTerminal Message', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        return

    def OnSerialRead(self, event):
        """Handle input from the serial port."""
        text = event.data
        p = max(text.rfind('\r'), text.rfind('\n'))
        if p >= 0:
            self.loginbuffer.append(text[:p + 1])
            s = ('').join(self.loginbuffer)
            self.loginbuffer = []
            self.loginbuffer.append(text[p + 1:])
            log.debug(':< %s' % makePrint(s))
        else:
            self.loginbuffer.append(text)
        if self.settings.unprintable:
            text = ('').join([ c >= ' ' and c or '<%d>' % ord(c) for c in text ])
        text = ScanBackspace(text)
        rep = {6: '<ACK>', 21: '<NACK>'}
        reps = ('').join([ chr(x) for x in rep.keys() ])
        text = ('').join([ x not in reps and x or rep[ord(x)] for x in text ])
        count = 0
        for c in text:
            if c == chr(8):
                count = count + 1
            else:
                break

        if count > 0:
            self.text_ctrl_output.SetEditable(1)
            curpos = self.text_ctrl_output.GetLastPosition()
            self.text_ctrl_output.Remove(curpos - count, curpos)
            self.text_ctrl_output.SetEditable(0)
            self.text_ctrl_output.SendTextUpdatedEvent()
        self.text_ctrl_output.AppendText(text[count:])

    def SerialThreadFunc(self):
        """Thread that handles the incomming traffic. Does the basic input
                   transformation (newlines) and generates an SerialRxEvent"""
        log.debug('Serial thread started')
        while self.SerialAlive.isSet():
            text = self.serial.read(100)
            if text:
                if self.settings.sp_newline == NEWLINE_NONE:
                    pass
                elif self.settings.sp_newline == NEWLINE_CR:
                    text = text.replace('\n', '\r')
                elif self.settings.sp_newline == NEWLINE_LF:
                    text = text.replace('\r', '\n')
                elif self.settings.sp_newline == NEWLINE_CRLF:
                    text = text.replace('\n\r', '\r\n')
                elif self.settings.sp_newline == NEWLINE_LFCR:
                    text = text.replace('\r\n', '\n\r')
                self.clients.write(text)
                event = SerialRxEvent(self.GetId(), text)
                self.GetEventHandler().AddPendingEvent(event)
            else:
                time.sleep(0.01)
            text = self.clients.read(-1)
            if text:
                self.handleKeys(text)

        log.debug('Serial thread stopped')

    def AppMsgThreadFunc(self):
        log.debug('AppMsg started')
        while self.AppMsgAlive.isSet():
            try:
                text = self.AppMsgQueue.get_nowait()
            except queues.Empty:
                time.sleep(0.25)
            else:
                if text:
                    event = AppMsgEvent(self.GetId(), text)
                    self.GetEventHandler().AddPendingEvent(event)

        log.debug('AppMsg stopped')


class TerminalApp_AskSettings(wx.App):

    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_terminal = TerminalFrame(None, -1, '')
        self.SetTopWindow(frame_terminal)
        frame_terminal.Show(1)
        return 1


class TerminalApp(wx.App):

    def __init__(self, *args, **kwds):
        self.Settings = DEF_SETTINGS
        for k in kwds.keys():
            if k in self.Settings.keys():
                self.Settings[k] = kwds[k]
                del kwds[k]

        if kwds.has_key('PortSettings'):
            self.Settings = kwds['PortSettings']
            del kwds['PortSettings']
        if kwds.has_key('AppMsgQueue'):
            self.AppMsgQueue = kwds['AppMsgQueue']
            del kwds['AppMsgQueue']
        else:
            self.AppMsgQueue = None
        wx.App.__init__(self, *args, **kwds)
        return

    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_terminal = TerminalFrame(None, -1, '', PortSettings=self.Settings, AppMsgQueue=self.AppMsgQueue)
        self.SetTopWindow(frame_terminal)
        frame_terminal.Show(1)
        return 1


def OneChar(string):
    if type(string) is str and len(string) > 0:
        return string[0]
    else:
        return ''


def ParseCLI():
    parser = argparse.ArgumentParser(description='A simple graphical terminal in pure wxPython')
    parser.add_argument('-port', type=str, help='Use <PORT>')
    parser.add_argument('-baud', type=int, dest='baudrate', metavar='BAUD', default=DEF_BAUD, help='Use BAUD rate (Default %s)' % DEF_BAUD)
    parser.add_argument('-snoopserver', type=int, default=DEF_SSPORT, help='Enable a data snooping telnet server')
    parser.add_argument('-xon', action='store_true', dest='xonxoff', help='Enable xon/xoff flow control')
    parser.add_argument('-rts', action='store_true', dest='rtscts', help='Enable hardware flow control')
    parser.add_argument('-timeout', type=float, default=DEF_TIMEOUT, help='Serial port read timeout in seconds (Default %1g)' % DEF_TIMEOUT)
    parser.add_argument('-echo', action='store_true', help='Enable local echo of tx data')
    parser.add_argument('-D', action='store_true', help='Enable debugging')
    parser.add_argument('-lockKB', action='store_true', help='Prevent keyboard input')
    group = parser.add_mutually_exclusive_group()
    for nl in NEWLINES:
        group.add_argument('-%s' % nl, dest='sp_newline', action='store_const', const=NEWLINES[nl], help='Enter is received as %s%s' % (nl, ' (Default)' if nl == DEF_SP_NEWLINE else ''))

    group.set_defaults(sp_newline=NEWLINES[DEF_SP_NEWLINE])
    group = parser.add_mutually_exclusive_group()
    for nl in NEWLINES:
        group.add_argument('-KB%s' % nl, dest='kb_newline', action='store_const', const=NEWLINES[nl], help='Enter Transmits %s%s' % (nl, ' (Default)' if nl == DEF_KB_NEWLINE else ''))

    group.set_defaults(kb_newline=NEWLINES[DEF_KB_NEWLINE])
    group = parser.add_mutually_exclusive_group()
    for n in (5, 6, 7, 8):
        group.add_argument('-SP%d' % n, dest='bytesize', action='store_const', const=n, help='Use %d bit data%s' % (n, ' (Default)' if n == DEF_BITS else ''))

    group.set_defaults(bytesize=DEF_BITS)
    parser.add_argument('-stop', type=float, dest='stopbits', choices=(1, 1.5, 2), default=DEF_STOP, help='Number of stop bits (Default %s)' % DEF_STOP)
    group = parser.add_mutually_exclusive_group()
    for p in PARITIES:
        group.add_argument('-%s' % p, dest='parity', action='store_const', const=p[0], help='%s parity%s' % (p, ' (Default)' if p == DEF_PARITY else ''))

    group.set_defaults(parity=DEF_PARITY[0])
    args = parser.parse_args()
    if args.D:
        log.setLevel(logging.DEBUG)
        con.setLevel(logging.DEBUG)
    return args


if __name__ == '__main__':
    pyver = sys.version.split(' ')[0].rsplit('.', 1)
    log.debug(pyver)
    args = ParseCLI()
    if args.port == None:
        app = TerminalApp_AskSettings(0)
    else:
        log.debug(args)
        PortKW = [ a for a in dir(args) if a[0] != '_' ]
        PortKV = [ args.__getattribute__(a) for a in PortKW ]
        PortSettings = dict(zip(PortKW, PortKV))
        app = TerminalApp(0, PortSettings=PortSettings)
    app.MainLoop()