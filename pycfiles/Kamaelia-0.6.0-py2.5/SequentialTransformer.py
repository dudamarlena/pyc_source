# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/SequentialTransformer.py
# Compiled at: 2008-10-19 12:19:52
"""================================
Sequential Transformer component
================================

This component applies all the functions supplied to incoming messages.
If the output from the final function is None, no message is sent.

Example Usage
-------------

To read in lines of text, convert to upper case, prepend "foo", and append "bar!"
and then write to the console::

    Pipeline(
        ConsoleReader(eol=""),
        SequentialTransformer( str,
                               str.upper,
                               lambda x : "foo" + x,
                               lambda x : x + "bar!",
                             ),
        ConsoleEchoer(),
    ).run()

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown

class SequentialTransformer(component):

    def __init__(self, *functions):
        super(SequentialTransformer, self).__init__()
        if len(functions) > 0:
            self.processMessage = self.pipeline
            self.functions = functions

    def processMessage(self, msg):
        pass

    def pipeline(self, msg):
        for function in self.functions:
            msg = function(msg)

        return msg

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
 SequentialTransformer,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    Pipeline(ConsoleReader(eol=''), SequentialTransformer(str, str.upper, lambda x: 'foo' + x, lambda x: x + 'bar!\n'), ConsoleEchoer()).run()