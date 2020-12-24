# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/ChunkNamer.py
# Compiled at: 2008-10-19 12:19:52
"""===========
Chunk Namer
===========

A component that labels each message with a unique filename for that message.
e.g. "A" ... "B" ... --> ["chunk1", "A"] ... ["chunk2", "B"] ...

Example Usage
-------------

Save each line entered to the console to a separate file::

    pipeline(
        ConsoleReader(),
        ChunkNamer("test", ".txt"),
        WholeFileWriter()
    ).run()

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

class ChunkNamer(component):
    """    ChunkNamer() -> new ChunkNamer component.
   
    Gives a filename to the chunk and sends it in the form [filename, contents],
    e.g. to a WholeFileWriter component.
   
    Keyword arguments:
    -- basepath - the prefix to apply to the filename
    -- suffix - the suffix to apply to the filename
    """
    Inboxes = {'inbox': 'Chunks to be saved', 
       'control': 'Shut me down'}
    Outboxes = {'outbox': 'List: [file name, file contents]', 
       'signal': "signal when I've shut down"}

    def __init__(self, basepath='', suffix=''):
        super(ChunkNamer, self).__init__()
        self.basepath = basepath
        self.suffix = suffix

    def main(self):
        buffer = ''
        chunknumber = 0
        while 1:
            yield 1
            while self.dataReady('inbox'):
                chunknumber += 1
                data = self.recv('inbox')
                command = [
                 self.basepath + 'chunk' + str(chunknumber) + self.suffix, data]
                self.send(command, 'outbox')

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), 'signal')
                    return

            self.pause()


__kamaelia_components__ = (ChunkNamer,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.File.WholeFileWriter import WholeFileWriter
    from Kamaelia.Util.Console import ConsoleReader
    pipeline(ConsoleReader(), ChunkNamer('test', '.txt'), WholeFileWriter()).run()