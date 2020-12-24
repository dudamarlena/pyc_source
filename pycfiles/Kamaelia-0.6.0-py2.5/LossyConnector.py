# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/LossyConnector.py
# Compiled at: 2008-10-19 12:19:52
"""====================================
Lossy connections between components
====================================

A component that passes on any data it receives, but will throw it away if the
next component's inbox is unable to accept new items.

Example Usage
-------------
Using a lossy connector to drop excess data::
    src = fastProducer().activate()
    lsy = LossyConnector().activate()
    dst = slowConsumer().activate()

    src.link( (src,"outbox"), (lsy,"inbox") )
    src.link( (lsy,"outbox"), (dst,"inbox"), pipewidth=1 )

The outbox of the lossy connector is joined to a linkage that can buffer a
maximum of one item. Once full, the lossy connector causes items to be dropped.

    

How does it work?
-----------------

This component receives data on its "inbox" inbox and immediately sends it on
out of its "oubox" outbox.

If the act of sending the data causes a noSpaceInBox exception, then it is
caught, and the data that it was trying to send is simply discarded.

I a producerFinished or shutdownMicroprocess message is received on the
component's "control" inbox, then the message is forwarded on out of its
"signal" outbox and the component then immediately terminates.
"""
from Axon.Component import component
from Axon.AxonExceptions import noSpaceInBox
from Axon.Ipc import producerFinished, shutdownMicroprocess

class LossyConnector(component):
    """    LossyConnector() -> new LossyConnector component

    Component that forwards data from inbox to outbox, but discards data if
    destination is full.
    """
    Inboxes = {'inbox': 'Data to be passed on', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': "Data received on 'inbox' inbox", 'signal': 'Shutdown signalling'}

    def mainBody(self):
        """Main loop body."""
        while self.dataReady('inbox'):
            try:
                self.send(self.recv())
            except noSpaceInBox:
                pass

        if self.dataReady('control'):
            mes = self.recv('control')
            if isinstance(mes, producerFinished) or isinstance(mes, shutdownMicroprocess):
                self.send(mes, 'signal')
                return 0
        return 1


__kamaelia_components__ = (
 LossyConnector,)