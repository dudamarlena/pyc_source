# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/Detuple.py
# Compiled at: 2008-10-19 12:19:52
import Axon
from Axon.Ipc import shutdownMicroprocess, producerFinished

class SimpleDetupler(Axon.Component.component):
    """
This class expects to recieve tuples (or more accurately
indexable objects) on its inboxes. It extracts the item
tuple[index] from the tuple (or indexable object) and
passes this out its outbox.

This component does not terminate.

This component was originally created for use with the
multicast component. (It could however be used for
extracting a single field from a dictionary like object).

Example usage::

    Pipeline(
        Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
        detuple(1), # Extract data, through away sender
        SRM_Receiver(),
        detuple(1),
        VorbisDecode(),
        AOAudioPlaybackAdaptor(),
    ).run()

"""

    def __init__(self, index):
        super(SimpleDetupler, self).__init__()
        self.index = index

    def main(self):
        shutdown = False
        while self.anyReady() or not shutdown:
            while self.dataReady('inbox'):
                tuple = self.recv('inbox')
                self.send(tuple[self.index], 'outbox')

            if not self.anyReady():
                self.pause()
            while self.dataReady('control'):
                msg = self.recv('control')
                self.send(msg, 'signal')
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    shutdown = True

            yield 1


__kamaelia_components__ = (SimpleDetupler,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline

    class TupleSauce(Axon.Component.component):

        def main(self):
            while 1:
                self.send(('greeting', 'hello', 'world'), 'outbox')
                yield 1


    class CheckResultIsHello(Axon.Component.component):

        def main(self):
            while 1:
                while self.dataReady('inbox'):
                    data = self.recv('inbox')
                    if data != 'hello':
                        print 'WARNING: expected', 'hello', 'received', data

                yield 1


    Pipeline(TupleSauce(), SimpleDetupler(1), CheckResultIsHello()).run()