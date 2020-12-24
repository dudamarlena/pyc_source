# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Internet/ThreadedTCPClient.py
# Compiled at: 2008-10-19 12:19:52
"""==========================
Simple Threaded TCP Client
==========================

This component is for making a TCP connection to a server. Send to its "inbox"
inbox to send data to the server. Pick up data received from the server on its
"outbox" outbox.

This component runs in its own separate thread so it can block on the socket
connection. This was written because some platforms that don't support
non-blocking calls to read/write data from sockets (eg. Python for
Nokia Series-60).

Example Usage
-------------

Sending the contents of a file to a server at address 1.2.3.4 on port 1000::

    Pipeline( RateControlledFileReader("myfile", rate=100000),
              ThreadedTCPClient("1.2.3.4", 1000),
            ).activate()

How does it work?
-----------------

The component opens a socket connection to the specified server on the specified
port. Data received over the connection appears at the component's "outbox"
outbox as strings. Data can be sent as strings by sending it to the "inbox"
inbox.

The component will shutdown in response to a producerFinished message arriving
on its "control" inbox. The socket will be closed, and a socketShutdown message
will be sent to the "signal" outbox.

All socket errors exceptions are passed on out of the "signal" outbox. This will
always result in the socket being closed (if open) and a socketShutdown message
also being sent to the "signal" outbox (after the exception).

It does not use a ConnectedSocketAdapter, instead handling all socket
communications itself.

The compnent is based on Axon.ThreadedComponent.threadedcomponent
"""
import socket, errno, Axon
from Axon.Component import component
from Kamaelia.IPC import socketShutdown
from Queue import Empty
import Axon.ThreadedComponent

class ThreadedTCPClient(Axon.ThreadedComponent.threadedcomponent):
    """   ThreadedTCPClient(host,port[,chargen][,initalsendmessage]) -> threaded component with a TCP connection to a server.

   Establishes a TCP connection to the specified server.
   
   Keyword arguments:
   
   - host     -- address of the server to connect to (string)
   - port     -- port number to connect on
   - initialsendmessage  -- to be send immediately after connection is established (default=None)
   """
    Inboxes = {'inbox': 'data to send to the socket', 'control': ''}
    Outboxes = {'outbox': 'data received from the socket', 'signal': 'diagnostic output, errors and shutdown messages'}

    def __init__(self, host, port, chargen=0, initialsendmessage=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        self.__super.__init__()
        self.host = host
        self.port = port
        self.chargen = chargen
        self.sendmessage = initialsendmessage

    def main(self):
        """Main (thread) loop"""
        try:
            self.send('Thread running', 'signal')
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, e:
                self.send(e, 'signal')
                self.send(socketShutdown(), 'signal')
                return

            self.send('socket object created', 'signal')
            try:
                sock.connect((self.host, self.port))
            except socket.error, e:
                self.send(e, 'signal')
                try:
                    result = sock.close()
                except:
                    pass
                else:
                    self.send(socketShutdown(), 'signal')
                    return

            self.send('socket connected', 'signal')
            producerFinished = 0
            if self.sendmessage != None:
                try:
                    sock.send(self.sendmessage)
                except socket.error, e:
                    self.send(e, 'signal')
                    try:
                        result = sock.close()
                    except:
                        pass
                    else:
                        self.send(socketShutdown(), 'signal')
                        return

            while 1:
                try:
                    data = sock.recv(1024)
                    if not data:
                        break
                    self.send(data)
                except socket.error, err:
                    self.send(err, 'signal')
                    break

                try:
                    if self.dataReady('control'):
                        msg = self.recv('control')
                        if isinstance(msg, Axon.Ipc.producerFinished):
                            break
                except Empty, e:
                    pass

            try:
                sock.shutdown(2)
            except socket.error, e:
                pass

            try:
                sock.close()
            except socket.error, e:
                self.send(e, 'signal')

            self.send(socketShutdown(), 'signal')
        except Exception, e:
            self.send('Unexpected exception', 'signal')
            self.send(e, 'signal')
            self.send(socketShutdown(), 'signal')

        return


__kamaelia_components__ = (ThreadedTCPClient,)
if __name__ == '__main__':
    from Axon.Scheduler import scheduler
    from Kamaelia.Util.Console import ConsoleEchoer
    from Axon.Ipc import newComponent
    from Kamaelia.Chassis.ConnectedServer import SimpleServer
    from Kamaelia.Protocol.FortuneCookieProtocol import FortuneCookieProtocol
    import Axon

    class testHarness(component):

        def __init__(self):
            self.__super.__init__()
            self.serverport = 4444
            self.server = SimpleServer(protocol=FortuneCookieProtocol, port=self.serverport)
            self.client = None
            self.display = ConsoleEchoer()
            self.displayerr = ConsoleEchoer()
            return

        def initialiseComponent(self):
            self.client = ThreadedTCPClient('127.0.0.1', self.serverport)
            self.addChildren(self.client, self.display, self.displayerr)
            self.addChildren(self.server, self.display)
            self.link((self.client, 'outbox'), (self.display, 'inbox'))
            self.link((self.client, 'signal'), (self.displayerr, 'inbox'))
            self.link((self, 'outbox'), (self.client, 'inbox'))
            print self.children
            return Axon.Ipc.newComponent(*self.children)

        def mainBody(self):
            return 1


    t = testHarness()
    t.activate()
    scheduler.run.runThreads(slowmo=0)