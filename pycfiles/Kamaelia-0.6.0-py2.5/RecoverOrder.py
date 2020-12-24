# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/RecoverOrder.py
# Compiled at: 2008-10-19 12:19:52
"""========================================
Recover Order of Sequence Numbered Items
========================================

Recovers the order of data tagged with sequence numbers. Designed to cope with
sequence numbers that have to eventually wrap.

Send (seqnum, data) tuples to the "inbox" inbox and they will be sent out of the
"outbox" outbox ordered by ascending sequence number.

Example Usage
-------------

Recovering the order of RTP packets received over multicast::
    
    Pipeline( Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
              SimpleDetupler(1),              # discard the source address
              RTPDeframer(),
              RecoverOrder(bufsize=64, modulo=65536),
              SimpleDetupler(1),              # discard sequence numbers
            ).activate()
    

Behaviour
---------

At initialisation, specify the size of buffer and the modulo (wrapping point)
for sequence numbers.

Send (seqnum, data) tuples to the "inbox" inbox and they will be buffered. Once
the buffer is full, for every item sent to the "inbox" inbox, one will be
emitted from the "outbox" outbox. The ones that are emitted will have been 
reordered by their sequence number.

You must ensure you choose a sufficiently large buffer size for the expected
amount of reordering required. If an item arrives too late, it RecoverOrder
will not be able to place it in its correct position in the sequence. It will
still be emitted, but out of order.

This component does not terminate. It ignores any messages sent to its "control"
inbox.

Implementation details
----------------------

The items are held in an internal buffer. The buffer is always in order - with
the earliest sequence number at the front. Once the buffer is full, items are
taken out from the front - thereby ensuring any delayed out-of-order items are
given every possible chance to make it.

Since sequence numbers eventually wrap, a given sequence number could equally
represent a data item that is very late, or very early.

This decision is made about a threshold - which is chosen to be the point in
the sequence number line roughly furthest from the sequence numbers of the 
items in the buffer. This point is the sequence number of the middle item in
the buffer, plus modulo/2::

       Data in the buffer
       .-------^--------.
       '                '
 |=====XX=X==XXXXXX=XX==X==================================================|
 |             ^                                    ^                      |
 0             |                                    |                    modulo
            midpoint                             midpoint
               |                                + modulo/2
 |<---LATE---->|<--------------EARLY--------------->|<------------LATE---->|
       A       |                 B                  |              C
                                              (aka. threshold)

Items with a sequence number after this threshold point are deemed to be late
(rather than ridiculously early). An item arriving with sequence number B
(marked above) has arrived early, and so should be appended to the end of the
data items in the buffer. Conversely, items arriving with sequence numbers A
or C (also marked above) must be late, so will be inserted at the front of the
buffer.

This is implemented by adding modulo to all sequence numbers below the threshold
when performing comparisons to determine where to insert the new sequence
number into the buffer (the insertion point is found by doing a binary search).
You can think of this as moving ranges A and B after range C.

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class RecoverOrder(component):
    """   RecoverOrder([bufsize][,modulo]) -> new RecoverOrder component.

   Receives and buffers (seqnum, data) pairs, and reorders them by ascending
   sequence number and emits them (when its internal buffer is full). This
   component can cope with the point at which sequence numbers wrap back to
   zero.
   
   Keyword arguments:
       
   - bufsize  -- Size of the buffer for data items (default=30)
   - modulo   -- Sequence numbers run from 0 to modulo-1 then wrap back to 0 (default=2**32)
   """

    def __init__(self, bufsize=30, modulo=4294967296):
        super(RecoverOrder, self).__init__()
        self.bufsize = bufsize
        self.modulo = modulo

    def main(self):
        """Main loop."""
        bufsize = self.bufsize
        datasource = []
        while 1:
            if not self.anyReady():
                self.pause()
            yield 1
            while self.dataReady('inbox'):
                item = self.recv('inbox')
                self.insertitem(datasource, item)
                if len(datasource) == bufsize:
                    try:
                        if datasource[0] != datasource[1]:
                            self.send(datasource[0], 'outbox')
                    except IndexError:
                        self.send(datasource[0], 'outbox')
                    else:
                        del datasource[0]

        need_clean_shutdown_make_this_true_and_fix = False
        if need_clean_shutdown_make_this_true_and_fix:
            while datasource != []:
                try:
                    if datasource[0] != datasource[1]:
                        self.send(datasource[0], 'outbox')
                except IndexError:
                    self.send(datasource[0], 'outbox')

                del datasource[0]

    def insertitem(self, buffer, item):
        if 0 == item[0] & 1023:
            print item[0]
        if len(buffer) == 0:
            buffer.insert(0, item)
        else:
            midindex = buffer[(len(buffer) / 2)][0]
            thresh = (midindex + self.modulo / 2) % self.modulo
            index = item[0]
            if index < thresh:
                index = index + self.modulo
            cmp = buffer[(-1)][0]
            if index <= cmp or index <= cmp + self.modulo:
                buffer.append(item)
            else:
                lo = -1
                hi = len(buffer)
                while hi - lo > 1:
                    mid = (lo + hi) / 2
                    midindex = buffer[mid][0]
                    if midindex < thresh:
                        midindex = midindex + self.modulo
                    if index < midindex:
                        hi = mid
                    else:
                        lo = mid

                buffer.insert(mid, item)