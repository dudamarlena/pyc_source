# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Internet/Multicast_transceiver.py
# Compiled at: 2008-10-19 12:19:52
"""============================
Simple multicast transceiver
============================

A simple component for transmitting and receiving multicast packets.

Remember that multicast is an unreliable connection - packets may be lost,
duplicated or reordered. 

Example Usage
-------------

Send a file to, and receive data from multicast group address 1.2.3.4 port 1000::

    Pipeline( RateControlledFileReader("myfile", rate=100000),
              Multicast_transceiver("0.0.0.0", 0, "1.2.3.4", 1000),
            ).activate()

    Pipeline( Multicast_transceiver("0.0.0.0", 1000, "1.2.3.4", 0)
              ConsoleEchoer()
            ).activate()

Or::
    
    Pipeline( RateControlledFileReader("myfile", rate=100000),
              Multicast_transceiver("0.0.0.0", 1000, "1.2.3.4", 1000),
              ConsoleEchoer()
            ).activate()

The data emitted by Multicast_transciever (and displayed by ConsoleEchoer) is of
the form (source_address, data).

More detail
-----------

Data sent to the component's "inbox" inbox is sent to the multicast group.

Data received from the multicast group is emitted as a tuple:
(source_addr, data) where data is a string of the received data.

This component ignores anything received on its "control" inbox. It is not yet
possible to ask it to shut down. It does not terminate.

Multicast groups do not 'shut down', so this component never emits any signals
on its "signal" outbox.

Why a transciever component?
----------------------------
Listens for packets in the given multicast group. Any data received is
sent to the receiver's outbox. The logic here is likely to be not quite
ideal. When complete though, this will be preferable over the sender and
receiver components since it models what multicast really is rather than
what people tend to think it is.
"""
import socket, Axon

class Multicast_transceiver(Axon.Component.component):
    """   Multicast_transciever(local_addr, local_port, remote_addr, remote_port) -> component that send and receives data to/from a multicast group.
    
   Creates a component that sends data received on its "inbox" inbox to the
   specified multicast group; and sends to its "outbox" outbox tuples of the
   form (src_addr, data) containing data received.
   
   Keyword arguments:
   
   - local_addr   -- local address (interface) to send from (string)
   - local_port   -- port number
   - remote_addr  -- address of multicast group (string)
   - remote_port  -- port number
   """
    Inboxes = {'inbox': 'Data to be sent to the multicast group', 'control': 'NOT USED'}
    Outboxes = {'outbox': 'Emits (src_addr, data_received)', 'signal': 'NOT USED'}

    def __init__(self, local_addr, local_port, remote_addr, remote_port, debug=False):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Multicast_transceiver, self).__init__()
        self.local_addr = local_addr
        self.local_port = local_port
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        self.debug = debug

    def main(self):
        """Main loop"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((self.local_addr, self.local_port))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        status = sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.remote_addr) + socket.inet_aton('0.0.0.0'))
        sock.setblocking(0)
        tosend = []
        while 1:
            try:
                (data, addr) = sock.recvfrom(16384)
            except socket.error, e:
                pass
            else:
                message = (
                 addr, data)
                self.send(message, 'outbox')

            yield 1
            while self.dataReady('inbox'):
                data = self.recv()
                tosend.append(data)

            if self.debug:
                print self.inboxes['inbox']
            while len(tosend) > 0:
                try:
                    l = sock.sendto(tosend[0], (self.remote_addr, self.remote_port))
                    del tosend[0]
                except socket.error, e:
                    break


def tests():
    print 'This module is acceptance tested as part of a system.'
    print 'Please see the test/test_MulticastTransceiverSystem.py script instead'


__kamaelia_components__ = (
 Multicast_transceiver,)
if __name__ == '__main__':
    tests()