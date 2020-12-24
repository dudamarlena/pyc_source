# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/File/TriggeredFileReader.py
# Compiled at: 2008-10-19 12:19:52
"""=======================
Triggered File Reader
=======================

This component accepts a filepath as an "inbox" message, and outputs the
contents of that file to "outbox". All requests are processed sequentially.

This component does not terminate.

Drawback - this component uses blocking file reading calls but does not
run on its own thread.
"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

class TriggeredFileReader(component):
    """    TriggeredFileReader() -> component that reads arbitrary files 
    """
    Inboxes = {'inbox': 'filepaths to read', 
       'control': 'Shut me down'}
    Outboxes = {'outbox': 'file contents, 1 per message', 
       'signal': 'Signal my shutdown with producerFinished'}

    def __init__(self):
        super(TriggeredFileReader, self).__init__()

    def readFile(self, filename):
        """Read data out of a file"""
        print 'readFile(' + filename + ')'
        file = open(filename, 'rb', 0)
        data = file.read()
        file.close()
        return data

    def main(self):
        """Main loop"""
        while 1:
            yield 1
            while self.dataReady('inbox'):
                command = self.recv('inbox')
                self.send(self.readFile(command), 'outbox')

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), 'signal')
                    return

            self.pause()


__kamaelia_components__ = (TriggeredFileReader,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    pipeline(ConsoleReader(eol=''), TriggeredFileReader(), ConsoleEchoer()).run()