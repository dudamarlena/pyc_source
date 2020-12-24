# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Internet/ConnectedSocketAdapter.py
# Compiled at: 2008-10-19 12:19:52
"""==========================
Talking to network sockets
==========================

A Connected Socket Adapter (CSA) component talks to a network server socket.
Data is sent to and received from the socket via this component's inboxes and
outboxes. A CSA is effectively a wrapper for a socket.

Most components should not need to create CSAs themselves. Instead, use
components such as TCPClient to make an outgoing connection, or TCPServer or
SimpleServer to be a server that responds to incoming connections.

Example Usage
-------------
See source code for TCPClient to see how Connected Socket Adapters can be used.

See also
--------
- TCPClient     -- for making a connection to a server
- TCPServer     -- 
- SimpleServer  -- a prefab chassis for building a server

How does it work?
-----------------
A CSA is usually created either by a component such as TCPClient that wants to
establish a connection to a server; or by a primary listener socket - a
component acting as a server - listening for incoming connections from clients.

The socket should be set up and passed to the constructor to make the CSA.

Incoming data, read by the CSA, is sent out of its "outbox" outbox as strings
containing the received binary data. Send data by sending it, as strings, to
the "inbox" outbox.

The CSA expects to be wired to a component that will notify it when new data
has arrived at its socket (by sending an Axon.Ipc.status message to its
"ReadReady" inbox. This is to allow the CSA to sleep rather than busy-wait or
blocking when waiting for new data to arrive. Typically this is the Selector
component.

This component will terminate (and close its socket) if it receives a
producerFinished message on its "control" inbox.

When this component terminates, it sends a socketShutdown(socket) message out of
its "CreatorFeedback" outbox and a shutdownCSA((selfCSA,self.socket)) message
out of its "signal" outbox.

The message sent to "CreatorFeedback" is to notify the original creator that
the socket is now closed and that this component should be unwired.

The message sent to the "signal" outbox serves to notify any other component
involved - such as the one feeding notifications to the "ReadReady" inbox (eg.
the Selector component).
"""
import socket, time, errno, Axon
from Axon.Component import component
from Axon.Ipc import wouldblock, status, producerFinished, shutdownMicroprocess
from Kamaelia.IPC import socketShutdown, newCSA, shutdownCSA
from Kamaelia.IPC import removeReader, removeWriter
from Kamaelia.IPC import newReader, newWriter, removeReader, removeWriter
from Kamaelia.KamaeliaExceptions import *
import traceback, pprint
whinge = {'socketSendingFailure': True, 'socketRecievingFailure': True}
crashAndBurn = {'uncheckedSocketShutdown': True, 'receivingDataFailed': True, 
   'sendingDataFailed': True}

class SSLSocket(object):

    def __init__(self, sock):
        self.sslobj = socket.ssl(sock)
        self.sock = sock

    def shutdown(self, code):
        self.sock.shutdown(code)

    def close(self):
        self.sock.close()

    def fileno(self):
        return self.sock.fileno()

    def setblocking(self, state):
        self.sock.setblocking(state)

    def recv(self, size=1024):
        try:
            return self.sslobj.read(size)
        except socket.sslerror, e:
            if e.args[0] not in [socket.SSL_ERROR_WANT_READ,
             socket.SSL_ERROR_WANT_WRITE]:
                raise
            return ''

    def send(self, data):
        try:
            return self.sslobj.write(data)
        except socket.sslerror, e:
            if e.args[0] not in [socket.SSL_ERROR_WANT_READ,
             socket.SSL_ERROR_WANT_WRITE]:
                raise
            return 0


class ConnectedSocketAdapter(component):
    """   ConnectedSocketAdapter(socket) -> new CSA component wrapping specified socket

   Component for communicating with a socket. Send to its "inbox" inbox to
   send data, and receive data from its "outbox" outbox.

   "ReadReady" inbox must be wired to something that will notify it when new
   data has arrived at the socket.
   """
    Inboxes = {'inbox': 'Data for this CSA to send through the socket (Axon.Ipc.status message)', 'control': 'Shutdown on producerFinished message (incoming & outgoing data is flushed first)', 
       'ReadReady': 'Notify this CSA that there is incoming data ready on the socket', 
       'SendReady': 'Notify this CSA that the socket is ready to send', 
       'makessl': 'Notify this CSA that the socket should be wrapped into SSL'}
    Outboxes = {'outbox': 'Data received from the socket', 'CreatorFeedback': "Expected to be connected to some form of signal input on the CSA's creator. Signals socketShutdown (this socket has closed)", 
       'signal': 'Signals shutdownCSA (this CSA is shutting down)', 
       '_selectorSignal': 'For communication to the selector', 
       'sslready': 'Notifies components that the socket is now wrapped into SSL'}

    def __init__(self, listensocket, selectorService, crashOnBadDataToSend=False, noisyErrors=True):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(ConnectedSocketAdapter, self).__init__()
        self.socket = listensocket
        self.data_to_send = ''
        self.crashOnBadDataToSend = crashOnBadDataToSend
        self.noisyErrors = noisyErrors
        self.selectorService = selectorService
        self.howDied = False
        self.isSSL = False
        self.couldnt_send = None
        return

    def handleControl(self):
        """Check for producerFinished message and shutdown in response"""
        if self.dataReady('control'):
            data = self.recv('control')
            if isinstance(data, producerFinished):
                self.connectionRECVLive = False
                self.connectionSENDLive = False
                self.howDied = 'producer finished'
            elif isinstance(data, shutdownMicroprocess):
                self.connectionRECVLive = False
                self.connectionSENDLive = False
                self.howDied = 'shutdown microprocess'

    def passOnShutdown(self):
        self.send(socketShutdown(self, [self.socket, self.howDied]), 'CreatorFeedback')
        self.send(shutdownCSA(self, (self, self.socket)), 'signal')

    def stop(self):
        self.socket.shutdown(2)
        self.socket.close()
        self.passOnShutdown()
        if self.socket is not None:
            self.send(removeReader(self, self.socket), '_selectorSignal')
            self.send(removeWriter(self, self.socket), '_selectorSignal')
        super(ConnectedSocketAdapter, self).stop()
        return

    def _safesend(self, sock, data):
        """Internal only function, used for sending data, and handling EAGAIN style
       retry scenarios gracefully"""
        bytes_sent = 0
        try:
            bytes_sent = sock.send(data)
            return bytes_sent
        except socket.error, socket.msg:
            (errorno, errmsg) = socket.msg.args
            if not (errorno == errno.EAGAIN or errorno == errno.EWOULDBLOCK):
                self.connectionSENDLive = False
                self.howDied = socket.msg
        except TypeError, ex:
            if self.noisyErrors:
                print 'CSA: Exception sending on socket: ', ex, '(no automatic conversion to string occurs).'
            if self.crashOnBadDataToSend:
                raise ex

        self.sending = False
        if self.connectionSENDLive:
            self.send(newWriter(self, ((self, 'SendReady'), sock)), '_selectorSignal')
        return bytes_sent

    def flushSendQueue(self):
        while len(self.data_to_send) != 0 or self.dataReady('inbox'):
            if len(self.data_to_send) == 0:
                self.data_to_send = self.recv('inbox')
            bytes_sent = self._safesend(self.socket, self.data_to_send)
            self.data_to_send = self.data_to_send[bytes_sent:]
            if bytes_sent == 0:
                break

    def _saferecv(self, sock, size=32768):
        """Internal only function, used for recieving data, and handling EAGAIN style
       retry scenarios gracefully"""
        try:
            data = sock.recv(size)
            if data:
                self.failcount = 0
                return data
            elif not self.isSSL:
                self.connectionRECVLive = False
        except socket.error, socket.msg:
            (errorno, errmsg) = socket.msg.args
            if not (errorno == errno.EAGAIN or errorno == errno.EWOULDBLOCK):
                self.connectionRECVLive = False
                self.howDied = socket.msg

        self.receiving = False
        if self.connectionRECVLive:
            self.send(newReader(self, ((self, 'ReadReady'), sock)), '_selectorSignal')
        return

    def handleReceive(self):
        successful = True
        while successful and self.connectionRECVLive:
            if self.couldnt_send is not None:
                try:
                    self.send(self.couldnt_send, 'outbox')
                    self.couldnt_send = None
                except Axon.AxonExceptions.noSpaceInBox:
                    return

            socketdata = self._saferecv(self.socket, 32768)
            if socketdata:
                try:
                    self.send(socketdata, 'outbox')
                except Axon.AxonExceptions.noSpaceInBox:
                    self.couldnt_send = socketdata
                    successful = False
                else:
                    successful = True
            else:
                successful = False

        return

    def checkSocketStatus(self):
        if self.dataReady('ReadReady'):
            self.receiving = True
            self.recv('ReadReady')
        if self.dataReady('SendReady'):
            self.sending = True
            self.recv('SendReady')

    def canDoSomething(self):
        if self.sending and (len(self.data_to_send) > 0 or self.dataReady('inbox')):
            return True
        if self.receiving:
            return True
        if self.anyReady():
            return True
        return False

    def main(self):
        self.link((self, '_selectorSignal'), self.selectorService)
        self.sending = True
        self.receiving = True
        self.connectionRECVLive = True
        self.connectionRECVLive = True
        self.connectionSENDLive = True
        while self.connectionRECVLive and self.connectionSENDLive:
            yield 1
            if self.dataReady('makessl'):
                self.recv('makessl')
                self.send(removeReader(self, self.socket), '_selectorSignal')
                self.send(removeWriter(self, self.socket), '_selectorSignal')
                self.socket.setblocking(True)
                self.socket = SSLSocket(self.socket)
                self.isSSL = True
                self.socket.setblocking(False)
                self.send(newReader(self, ((self, 'ReadReady'), self.socket)), '_selectorSignal')
                self.send(newWriter(self, ((self, 'SendReady'), self.socket)), '_selectorSignal')
                self.send('', 'sslready')
                yield 1
            self.checkSocketStatus()
            self.handleControl()
            if self.sending:
                self.flushSendQueue()
            if self.receiving:
                self.handleReceive()
            if not self.canDoSomething():
                self.pause()

        self.passOnShutdown()


__kamaelia_components__ = (
 ConnectedSocketAdapter,)