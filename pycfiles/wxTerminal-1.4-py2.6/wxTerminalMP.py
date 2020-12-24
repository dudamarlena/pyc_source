# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wxTerminal/wxTerminalMP.py
# Compiled at: 2013-01-24 05:44:52
"""This is a multiprocessing wrapper for wxTerminal that allows you to embed a wxTerminal
within another application, for instance this allows the application to use snooping to
provide real access to the port, while the application uses the snoop port to talk to
the wxTerminal, e.g.

t=Terminal(port='/dev/ttyS0',baudrate=115200,snoopserver=56712)
s=serial.serial_for_url("socket://localhost:56712")
s.write("Test")
result=s.read()
s.close()
t.close()
"""
import multiprocessing, wxtMsg, wxTerminal

class TerminalMP(object):
    """A wxTerminal wrapped in multiprocessing to support snooping"""

    def __init__(self, *args, **kwds):
        self.q = multiprocessing.Queue()
        kwds['AppMsgQueue'] = self.q
        self.p = multiprocessing.Process(target=self.getApp, args=(args, kwds))
        self.p.start()

    def close(self):
        self._appMsg(wxtMsg.AM_QUIT, 'QUIT!')
        self.q.close()
        self.q.join_thread()
        self.p.join()

    def getApp(self, args, kwds):
        app = wxTerminal.TerminalApp(0, *args, **kwds)
        app.MainLoop()

    def _appMsg(self, msgtype, data):
        self.q.put((msgtype, data))

    def Dialog(self, msg):
        self._appMsg(wxtMsg.AM_DIALOG, msg)


def Terminal(*args, **kwds):
    return TerminalMP(*args, **kwds)


def USB0():
    return Terminal(port='/dev/ttyUSB0', baudrate=57600)


def USB1():
    return Terminal(port='/dev/ttyUSB1', baudrate=115200)