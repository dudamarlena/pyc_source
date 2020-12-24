# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Internet/Multicast_receiver.py
# Compiled at: 2008-10-19 12:19:52
"""=========================
Simple multicast receiver
=========================

A simple component for receiving packets in the specified multicast group.

Remember that multicast is an unreliable connection - packets may be lost,
duplicated or reordered. 

Example Usage
-------------

Receiving multicast packets from group address 1.2.3.4 port 1000 and displaying
them on the console::

    Pipeline( Multicast_receiver("1.2.3.4", 1000),
              ConsoleEchoer()
            ).activate()

The data emitted by Multicast_receiver (and displayed by ConsoleEchoer) is of
the form (source_address, data).

More detail
-----------

Data received from the multicast group is emitted as a tuple:
(source_addr, data) where data is a string of the received data.

This component ignores anything received on its "control" inbox. It is not yet
possible to ask it to shut down. It does not terminate.

Multicast groups do not 'shut down', so this component never emits any signals
on its "signal" outbox.
"""
import socket, Axon

class Multicast_receiver(Axon.Component.component):
    """    Multicast_receiver(address, port) -> component that receives multicast traffic.

    Creates a component that receives multicast packets in the given multicast group
    and sends it out of its "outbox" outbox.
    
    Keyword arguments:
    
    - address  -- address of multicast group (string)
    - port     -- port number
    """
    Inboxes = {'inbox': 'NOT USED', 'control': 'NOT USED'}
    Outboxes = {'outbox': 'Emits (src_addr, data_received)', 'signal': 'NOT USED'}

    def __init__(self, address, port):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Multicast_receiver, self).__init__()
        self.mcast_addr = address
        self.port = port

    def main(self):
        """Main loop"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((self.mcast_addr, self.port))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        status = sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.mcast_addr) + socket.inet_aton('0.0.0.0'))
        sock.setblocking(0)
        while 1:
            try:
                (data, addr) = sock.recvfrom(1024)
            except socket.error, e:
                pass
            else:
                message = (
                 addr, data)
                self.send(message, 'outbox')

            yield 1


def tests():
    from Axon.Scheduler import scheduler
    from Kamaelia.Util.Console import ConsoleEchoer

    class testComponent(Axon.Component.component):

        def main(self):
            receiver = Multicast_receiver('224.168.2.9', 1600)
            display = ConsoleEchoer()
            self.link((receiver, 'outbox'), (display, 'inbox'))
            self.addChildren(receiver, display)
            yield Axon.Ipc.newComponent(*self.children)
            while 1:
                self.pause()
                yield 1

    harness = testComponent()
    harness.activate()
    scheduler.run.runThreads(slowmo=0.1)


__kamaelia_components__ = (
 Multicast_receiver,)
if __name__ == '__main__':
    tests()