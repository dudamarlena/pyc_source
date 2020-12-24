# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/NullSink.py
# Compiled at: 2008-10-19 12:19:52
"""
Null sink component.  To ignore a component's outbox connect it to this
component and the box will be emptied but not used in any way.  This will be
necessary with syncronized linkages.
"""
from Axon.Component import component, scheduler
from Axon.Ipc import producerFinished, shutdownMicroprocess

class nullSinkComponent(component):
    Inboxes = [
     'inbox', 'control']
    Outboxes = ['outbox', 'signal']

    def mainBody(self):
        while self.dataReady('inbox'):
            data = self.recv('inbox')

        if self.dataReady('control'):
            data = self.recv('control')
            if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
                return 0
        return 1


__kamaelia_components__ = (
 nullSinkComponent,)
if __name__ == '__main__':
    print 'This module has no system test'