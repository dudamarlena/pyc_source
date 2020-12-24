# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Visualisation/PhysicsGraph/chunks_to_lines.py
# Compiled at: 2008-10-19 12:19:52
r"""==================
Text line splitter
==================

This component takes chunks of text and splits them at line breaks into
individual lines.

Example usage
-------------
A system that connects to a server and receives fragmented text data, but then
displays it a whole line at a time::

    Pipeline( TCPClient(host=..., port=...),
      chunks_to_lines(),
      ConsoleEcho()
    ).run()
            

            
How does it work?
-----------------

chunks_to_lines buffers all text it receives on its "inbox" inbox. If there is a
line break ("\n") in the text it has buffered, then it extracts that line of
text, including the line break character and sends it on out of its "outbox"
outbox.

It also removes any "\r" characters in the text.

If a producerFinished() or shutdownMicroprocess() message is received on this
component's "control" inbox, then it will send it on out of its "signal" outbox
and immediately terminate. It will not flush any whole lines of text that may
still be buffered.
"""
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

class chunks_to_lines(component):
    """   chunks_to_lines() -> new chunks_to_lines component.
   
   Takes in chunked textual data and splits it at line breaks into individual
   lines.
   """
    Inboxes = {'inbox': 'Chunked textual data', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': 'Individual lines of text', 'signal': 'Shutdown signalling'}

    def main(self):
        """Main loop."""
        gotLine = False
        line = ''
        while not self.shutdown():
            while self.dataReady('inbox'):
                chunk = self.recv('inbox')
                chunk = chunk.replace('\r', '')
                line = line + chunk

            pos = line.find('\n')
            while pos > -1:
                self.send(line[:pos], 'outbox')
                line = line[pos + 1:]
                pos = line.find('\n')

            self.pause()
            yield 1

    def shutdown(self):
        """      Returns True if a shutdownMicroprocess or producerFinished message was received.
      """
        while self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send(msg, 'signal')
                return True

        return False


__kamaelia_components__ = (
 chunks_to_lines,)