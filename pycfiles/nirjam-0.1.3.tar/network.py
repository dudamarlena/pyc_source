# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Git/nirjam/nirjam/traffic/network.py
# Compiled at: 2016-10-12 18:43:21
try:
    import thread
except ImportError:
    import _thread as thread

import socket, time
SERVER_HOST = '0.0.0.0'
PORT = 8888
BUFFER_SIZE = 1024

def trace(msg):
    pass


class Connection:

    def defaultWhenHungupHandler(self):
        print 'CONNECTION LOST'
        self.connected = False

    port = PORT
    interface = SERVER_HOST
    whenHungupHandler = defaultWhenHungupHandler
    connected = False
    myHandle = None
    peerHandle = None
    threadHandle = None
    startOfPacket = None
    endOfPacket = None

    def trace(self, msg):
        trace(msg)

    def whenHungUp(self, thenCallFunction):
        if thenCallFunction == None:
            self.whenHungupHandler = self.defaultWhenHungupHandler
        else:
            self.whenHungupHandler = thenCallFunction
        return

    def call(self, addr, whenHearCall, port=None):
        self.trace('call:' + addr)
        if port != None:
            self.port = port
        else:
            self.port = PORT
        self.peerHandle = _clientOpen(addr, self.port)
        self.connected = True
        self.threadHandle = _startListenerThread(self.peerHandle, addr, whenHearCall, self.whenHungupHandler, self.endOfPacket)
        return

    def wait(self, whenHearCall, port=None):
        self.trace('wait')
        if port != None:
            self.port = port
        else:
            self.port = PORT
        self.myHandle = _serverWait(self.interface, self.port)
        self.peerHandle, addr = _serverAccept(self.myHandle)
        self.connected = True
        self.threadHandle = _startListenerThread(self.peerHandle, addr, whenHearCall, self.whenHungupHandler, self.endOfPacket)
        return

    def isConnected(self):
        self.trace('isConnected:' + str(self.connected))
        return self.connected

    def say(self, data):
        self.trace('say:' + data)
        if self.peerHandle == None:
            self.trace('say called hangup')
            self.hangUp()
        else:
            if self.startOfPacket != None:
                data = self.startOfPacket + data
            if self.endOfPacket != None:
                data = data + self.endOfPacket
            _send(self.peerHandle, data)
        return

    def hangUp(self):
        self.trace('hangup')
        self.whenHungupHandler()
        self.connected = False
        if self.threadHandle != None:
            _stopListenerThread(self.threadHandle)
            self.threadHandle = None
        if self.peerHandle != None:
            _close(self.peerHandle)
            self.peerHandle = None
        if self.myHandle != None:
            _close(self.myHandle)
            self.myHandle = None
        return


class TextConnection(Connection):

    def __init__(self):
        self.endOfPacket = '\r\n'


class BinaryConnection(Connection):

    def __init__(self):
        self.endOfPacket = None
        return


def _startListenerThread(handle, addr, whenHearFn, hangUpFn, packetiser):
    return thread.start_new_thread(_listenerThreadBody, (handle, addr, whenHearFn, hangUpFn, packetiser))


def _stopListenerThread(threadHandle):
    trace('_stopListenerThread')


def _listenerThreadBody(handle, addr, whenHearFn, hangUpFn=None, packetiser=None):
    trace('_listenerThreadBody:' + str(addr))
    buffer = ''
    while True:
        try:
            data = _receive(handle, hangUpFn)
            if data == None or len(data) == 0:
                trace('threadbody none or 0-data, called hangup')
                if hangUpFn != None:
                    hangUpFn()
                return
        except:
            trace('threadBody exception hangup')
            if hangUpFn != None:
                hangUpFn()
            return

        data = data.decode('utf-8')
        if packetiser == None:
            if whenHearFn != None:
                whenHearFn(data)
        else:
            for ch in data:
                if ch == '\r':
                    pass
                elif ch != '\n':
                    buffer += ch
                else:
                    if whenHearFn != None:
                        whenHearFn(buffer)
                    buffer = ''

    return


def _clientOpen(addr, port):
    trace('open:' + addr)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr, port))
    return s


def _serverWait(addr, port):
    trace('wait connection')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, port))
    s.listen(1)
    return s


def _serverAccept(handle):
    trace('accept')
    handle2, addr = handle.accept()
    trace('Connected by:' + str(addr))
    return (handle2, addr)


def _close(handle):
    trace('close')
    handle.close()


def _send(handle, data):
    trace('send:' + data)
    data = data.encode('utf-8')
    handle.sendall(data)


def _receive(handle, hangUpFn=None):
    trace('receive')
    try:
        data = handle.recv(BUFFER_SIZE)
        if data == None:
            trace('receive data none hangup')
            if hangUpFn != None:
                hangUpFn()
    except:
        if hangUpFn != None:
            hangUpFn()
            return

    return data


conn = TextConnection()

def whenHungUp(thenCallFunction):
    conn.whenHungUp(thenCallFunction)


def call(addr, whenHearCall=None, port=None):
    conn.call(addr, whenHearCall, port=port)


def wait(whenHearCall, port=None):
    conn.wait(whenHearCall, port)


def isConnected():
    return conn.isConnected()


def say(data):
    conn.say(data)


def hangUp():
    conn.hangUp()