# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/Sync.py
# Compiled at: 2008-10-19 12:19:52
"""================================================
Wait for 'n' items before sending one of them on
================================================

For every 'n' items received, one is sent out (the first one received in the
latest batch).

Example Usage
-------------

Wait for two tasks to finish, before propagating the shutdown message::

    Graphline( A    = TaskA(),
               B    = TaskB(),
               SYNC = Sync(2),
               linkages = {
                   ("A", "signal") : ("SYNC", "inbox"),
                   ("B", "signal") : ("SYNC", "inbox"),

                   ("SYNC", "outbox") : ("SYNC", "control"),
                   ("SYNC", "signal") : ("", "signal"),
               }

The slightly strange wiring is to make sure the Sync component is also shut
down. The shutdown message is used to shutdown Sync itself. The shutdown message
it emits is then the one that propogates out of the graphline.

Behaviour
---------

At initialisation, specify the number of items Sync should wait for.

Once that number of items have arrived at Sync's "inbox" inbox; the first that
arrived is sent on out of its "outbox" outbox. This process is repeated until
Sync is shut down.

If more han the specified number of items arrive in one go; the excess items
roll over to the next cycle. They are not ignored or lost.

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox. It is immediately sent on out of the "signal" outbox and the
component then immediately terminates.

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Sync(component):
    """    Sync([n]) -> new Sync component.
    
    After ever 'n' items received, the first in each batch received is sent on.
    
    Keyword arguments::
        
    - n  -- The number of items to expect (default=2)
    """
    Inboxes = {'inbox': 'Data items', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': 'First data item from last batch', 'signal': 'Shutdown signalling'}

    def __init__(self, n=2):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Sync, self).__init__()
        self.n = n

    def main(self):
        """Main loop"""
        while 1:
            for i in range(self.n):
                while not self.dataReady('inbox'):
                    while self.dataReady('control'):
                        msg = self.recv('control')
                        self.send(msg, 'signal')
                        if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                            return

                    self.pause()
                    yield 1

                data = self.recv('inbox')

            self.send(data, 'outbox')


__kamaelia_components__ = (
 Sync,)