# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/PureTransformer.py
# Compiled at: 2008-10-19 12:19:52
"""==========================
Pure Transformer component
==========================

This component applies a function specified at its creation to messages
received (a filter). If the function returns None, no message is sent,
otherwise the result of the function is sent to "outbox".

Example Usage
-------------

To read in lines of text, convert to upper case and then write to the console::
    
    Pipeline(
        ConsoleReader(),
        PureTransformer(lambda x : x.upper()),
        ConsoleEchoer()
    ).run()

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown

class PureTransformer(component):

    def __init__(self, function=None):
        super(PureTransformer, self).__init__()
        if function:
            self.processMessage = function

    def processMessage(self, msg):
        pass

    def main(self):
        while 1:
            yield 1
            while self.dataReady('inbox'):
                returnval = self.processMessage(self.recv('inbox'))
                if returnval != None:
                    self.send(returnval, 'outbox')

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), 'signal')
                    return

            self.pause()

        return


__kamaelia_components__ = (
 PureTransformer,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    pipeline(ConsoleReader(eol=''), PureTransformer(lambda x: 'foo' + x + 'bar!\n'), ConsoleEchoer()).run()