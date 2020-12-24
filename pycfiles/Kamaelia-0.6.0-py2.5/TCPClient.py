# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Internet/TCPClient.py
# Compiled at: 2008-10-19 12:19:52
"""=================
Simple TCP Client
=================

This component is for making a TCP connection to a server. Send to its "inbox"
inbox to send data to the server. Pick up data received from the server on its
"outbox" outbox.

Example Usage
-------------

Sending the contents of a file to a server at address 1.2.3.4 on port 1000::

    Pipeline( RateControlledFileReader("myfile", rate=100000),
              TCPClient("1.2.3.4", 1000),
            ).activate()

Example Usage - SSL
-------------------

It is also possible to cause the TCPClient to switch into SSL mode. To do this
you send it a message on its "makessl" inbox. It is necessary for a number of
protocols to be able to switch between non-ssl and ssl, hence this approach
rather than simply saying "ssl client" or "non-ssl client"::

    Graphline(
           MAKESSL = OneShot(" make ssl "),
           CONSOLE = ConsoleReader(),
           ECHO = ConsoleEchoer(),
           CONNECTION = TCPClient("kamaelia.svn.sourceforge.net", 443),
           linkages = {
               ("MAKESSL", "outbox"): ("CONNECTION", "makessl"),
               ("CONSOLE", "outbox"): ("CONNECTION", "inbox"),
               ("CONNECTION", "outbox"): ("ECHO", "inbox"),
           }
    )

How does it work?
-----------------

TCPClient opens a socket connection to the specified server on the specified
port. Data received over the connection appears at the component's "outbox"
outbox as strings. Data can be sent as strings by sending it to the "inbox"
inbox.

An optional delay (between component activation and attempting to connect) can
be specified. The default is no delay.

It creates a ConnectedSocketAdapter (CSA) to handle the socket connection and
registers it with a selectorComponent so it is notified of incoming data. The
selectorComponent is obtained by calling
selectorComponent.getSelectorService(...) to look it up with the local
Coordinating Assistant Tracker (CAT).

TCPClient wires itself to the "CreatorFeedback" outbox of the CSA. It also wires
its "inbox" inbox to pass data straight through to the CSA's "inbox" inbox,
and its "outbox" outbox to pass through data from the CSA's "outbox" outbox.

Socket errors (after the connection has been successfully established) may be
sent to the "signal" outbox.

This component will terminate if the CSA sends a socketShutdown message to its
"CreatorFeedback" outbox.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to its "control" inbox. This message is forwarded onto the CSA.
TCPClient will then wait for the CSA to terminate. It then sends its own
shutdownMicroprocess message out of the "signal" outbox.
"""
import socket, errno, Axon
from Axon.util import Finality
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.Ipc import newComponent, status
from Kamaelia.IPC import socketShutdown, newCSA
from Kamaelia.IPC import newReader, newWriter
from Kamaelia.IPC import removeReader, removeWriter
from Kamaelia.Internet.ConnectedSocketAdapter import ConnectedSocketAdapter
from Kamaelia.Internet.Selector import Selector

class TCPClient(Axon.Component.component):
    """   TCPClient(host,port[,delay]) -> component with a TCP connection to a server.

   Establishes a TCP connection to the specified server.
   
   Keyword arguments:
   
   - host     -- address of the server to connect to (string)
   - port     -- port number to connect on
   - delay    -- delay (seconds) after activation before connecting (default=0)
   """
    Inboxes = {'inbox': 'data to send to the socket', '_socketFeedback': 'notifications from the ConnectedSocketAdapter', 
       'control': 'Shutdown signalling', 
       'makessl': 'Notifications to the ConnectedSocketAdapter that we want to negotiate SSL'}
    Outboxes = {'outbox': 'data received from the socket', 'signal': 'socket errors', 
       '_selectorSignal': 'For registering and deregistering ConnectedSocketAdapter components with a selector service', 
       'sslready': 'SSL negotiated successfully'}
    Usescomponents = [
     ConnectedSocketAdapter]

    def __init__(self, host, port, delay=0):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(TCPClient, self).__init__()
        self.host = host
        self.port = port
        self.delay = delay
        self.CSA = None
        self.sock = None
        self.howDied = None
        return

    def main(self):
        """Main loop."""
        import time
        t = time.time()
        while time.time() - t < self.delay:
            yield 1

        for v in self.runClient():
            yield v

        if self.sock is not None and self.CSA is not None:
            self.send(removeReader(self.CSA, self.sock), '_selectorSignal')
            self.send(removeWriter(self.CSA, self.sock), '_selectorSignal')
        return

    def setupCSA(self, sock):
        """      setupCSA(sock) -> new ConnectedSocketAdapter component

      Creates a ConnectedSocketAdapter component for the socket, and wires up to
      it. Also sends the CSA to the "selector" service.
      """
        (selectorService, selectorShutdownService, newSelector) = Selector.getSelectorServices(self.tracker)
        if newSelector:
            self.addChildren(newSelector)
        CSA = ConnectedSocketAdapter(sock, selectorService)
        self.addChildren(CSA)
        self.link((self, '_selectorSignal'), selectorService)
        self.link((CSA, 'CreatorFeedback'), (self, '_socketFeedback'))
        self.link((CSA, 'outbox'), (self, 'outbox'), passthrough=2)
        self.link((CSA, 'sslready'), (self, 'sslready'), passthrough=2)
        self.link((self, 'inbox'), (CSA, 'inbox'), passthrough=1)
        self.link((self, 'makessl'), (CSA, 'makessl'), passthrough=1)
        self.link((self, 'control'), (CSA, 'control'), passthrough=1)
        self.send(newReader(CSA, ((CSA, 'ReadReady'), sock)), '_selectorSignal')
        self.send(newWriter(CSA, ((CSA, 'SendReady'), sock)), '_selectorSignal')
        self.CSA = CSA
        return self.childComponents()

    def waitCSAClose(self):
        """Returns True if a socketShutdown message is received on "_socketFeedback" inbox."""
        if self.dataReady('_socketFeedback'):
            message = self.recv('_socketFeedback')
            if isinstance(message, socketShutdown):
                try:
                    (socket, howdied) = message
                    self.howDied = howdied
                except TypeError:
                    self.howDied = None
                else:
                    return False
        return True

    def safeConnect(self, sock, *sockArgsList):
        """      Connect to socket and handle possible errors that may occur.

      Returns True if successful, or False on failure. Unhandled errors are raised
      as exceptions.
      """
        try:
            sock.connect(*sockArgsList)
            self.connecting = 0
            return True
        except socket.error, socket.msg:
            (errorno, errmsg) = socket.msg.args
            if errorno == errno.EALREADY:
                assert self.connecting == 1
                return False
            elif errorno == errno.EINPROGRESS or errorno == errno.EWOULDBLOCK:
                self.connecting = 1
                return False
            elif errorno == errno.EISCONN:
                self.connecting = 0
                return True
            elif hasattr(errno, 'WSAEINVAL'):
                if errorno == errno.WSAEINVAL:
                    assert self.connecting == 1
                    return False
            else:
                raise socket.msg

    def runClient(self, sock=None):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            yield 0.3
            self.sock = sock
            try:
                sock.setblocking(0)
                yield 0.6
                try:
                    while not self.safeConnect(sock, (self.host, self.port)):
                        if self.shutdown():
                            return
                        yield 1

                    yield newComponent(*self.setupCSA(sock))
                    while self.waitCSAClose():
                        self.pause()
                        yield 2

                    raise Finality
                except Exception, x:
                    result = sock.shutdown(2)
                    yield 3
                    raise x

            except Exception, x:
                sock.close()
                yield (4, x)
                raise x

        except Finality:
            yield 5
        except socket.error, e:
            pass

        self.send(producerFinished(self, self.howDied), 'signal')

    def shutdown(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return True

        return False


__kamaelia_components__ = (
 TCPClient,)
if __name__ == '__main__':
    from Axon.Scheduler import scheduler
    from Kamaelia.Chassis.ConnectedServer import SimpleServer
    from Kamaelia.Protocol.FortuneCookieProtocol import FortuneCookieProtocol
    from Kamaelia.Util.Console import ConsoleEchoer
    from Axon.Component import component

    class testHarness(component):

        def __init__(self):
            super(testHarness, self).__init__()
            import random
            self.serverport = random.randint(4000, 8000)
            self.server = SimpleServer(protocol=FortuneCookieProtocol, port=self.serverport)
            self.client = None
            self.display = ConsoleEchoer()
            return

        def initialiseComponent(self):
            self.client = TCPClient('127.0.0.1', self.serverport, delay=1)
            self.addChildren(self.server, self.client, self.display)
            self.link((self.client, 'outbox'), (self.display, 'inbox'))
            return Axon.Ipc.newComponent(*self.children)

        def mainBody(self):
            return 1


    t = testHarness()
    t.activate()
    scheduler.run.runThreads(slowmo=0)