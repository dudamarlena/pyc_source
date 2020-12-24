# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/FirstOnly.py
# Compiled at: 2008-10-19 12:19:52
"""===========================
Pass on the first item only
===========================

The first item sent to FirstOnly will be passed on. All other items are ignored.

Example Usage
-------------

Displaying the frame rate, just once, from video when it is decoded::

    Pipeline( ...
              DiracDecoder(),
              FirstOnly(),
              SimpleDetupler("frame_rate"),
              ConsoleEchoer(),
            )

Behaviour
---------

The first data item sent to FirstOnly's "inbox" inbox is immediately sent on
out of its "outbox" outbox.

Any subsequent data sent to its "inbox" inbox is discarded.

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox. It is immediately sent on out of the "signal" outbox and the
component then immediately terminates.

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class FirstOnly(component):
    """    FirstOnly() -> new FirstOnly component.

    Passes on the first item sent to it, and discards everything else.
    """
    Inboxes = {'inbox': 'Data items', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': 'First data item received', 'signal': 'Shutdown signalling'}

    def main(self):
        """Main loop"""
        while not self.dataReady('inbox'):
            if self.dataReady('control'):
                self.send(self.recv('control'), 'signal')
                return
            self.pause()
            yield 1

        self.send(self.recv('inbox'), 'outbox')
        while not self.dataReady('control'):
            while self.dataReady('inbox'):
                self.recv('inbox')

            self.pause()
            yield 1

        self.send(self.recv('control'), 'signal')


__kamaelia_components__ = (
 FirstOnly,)