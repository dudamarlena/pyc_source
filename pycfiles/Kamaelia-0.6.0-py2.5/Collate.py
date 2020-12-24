# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/Collate.py
# Compiled at: 2008-10-19 12:19:52
"""=================================================
Collate everything received into a single message
=================================================

Buffers all data sent to it. When shut down, sends all data it has received as
collated as a list in a single message.

Example Usage
-------------

Read a file, in small chunks, then collate them into a single chunk::
    
    Pipeline( RateControlledFileReader("big_file", ... ),
              Collate(),
              ...
            )
            

Behaviour
---------

Send data items to its "inbox" inbox to be collated.

Send a producerFinished or shutdownMicroprocess message to the "control" inbox
to terminate this component. 

All collated data items will be sent out of the "outbox" outbox as a list in a
single message. The items are collated in the same order they first arrived.

The component will then send on the shutdown message to its "signal" outbox and
immediately terminate.

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Collate(component):
    """    Collate() -> new Collate component.
    
    Buffers all data sent to it. When shut down, sends all data it has received
    as a single message.
    """
    Inboxes = {'inbox': 'Data items', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': 'All data items collated into one message', 'signal': 'Shutdown signalling'}

    def main(self):
        """Main loop"""
        collated = []
        while 1:
            while self.dataReady('inbox'):
                collated.append(self.recv('inbox'))

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    self.send(collated, 'outbox')
                    self.send(msg, 'signal')
                    return
                else:
                    self.send(msg, 'signal')

            self.pause()
            yield 1


__kamaelia_components__ = (Collate,)