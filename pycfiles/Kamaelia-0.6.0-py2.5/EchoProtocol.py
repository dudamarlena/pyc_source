# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/EchoProtocol.py
# Compiled at: 2008-10-19 12:19:52
"""
====================
Simple Echo Protocol
====================

A simple protocol component that echoes back anything sent to it.

It simply copies its input to its output.

Example Usage
-------------

A simple server that accepts connections on port 1501, echoing back anything sent
to it::

    >>> SimpleServer(protocol=EchoProtocol, port=1501).run()

On a unix/linux client::

    > telnet <server ip> 1501
    Trying <server ip>...
    Connected to <server ip>...
    hello world, this will be echoed back when I press return (newline)
    hello world, this will be echoed back when I press return (newline)
    oooh, thats nice!
    oooh, thats nice!

How does it work?
-----------------

The component receives data on its "inbox" inbox and immediately copies it to
its "outbox" outbox.

If a producerFinished or shutdownMicroprocess message is received on its
"control" inbox, the component sends a producerFinished message to its "signal"
outbox and terminates.
"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class EchoProtocol(component):
    """   EchoProtocol() -> new EchoProtocol component

   Simple component that copies anything sent to its "inbox" inbox to its "outbox"
   outbox.
   """

    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(EchoProtocol, self).__init__()

    def mainBody(self):
        """Main body."""
        self.pause()
        while self.dataReady('inbox'):
            data = self.recv('inbox')
            self.send(data, 'outbox')

        return self.shutdown()

    def shutdown(self):
        """Return 0 if a shutdown message is received, else return 1."""
        while self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(producerFinished(self), 'signal')
                return 0

        return 1


__kamaelia_components__ = (
 EchoProtocol,)
if __name__ == '__main__':
    from Kamaelia.Chassis.ConnectedServer import SimpleServer
    SimpleServer(protocol=EchoProtocol, port=1501).run()