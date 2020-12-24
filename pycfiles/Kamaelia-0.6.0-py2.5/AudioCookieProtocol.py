# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/AudioCookieProtocol.py
# Compiled at: 2008-10-19 12:19:52
"""
==============================================
Simple "Audio fortune cookie" Protocol Handler
==============================================

A simple protocol handler that simply sends the contents of a randomly chosen
audio file to the client.

Example Usage
-------------
::
    >>> SimpleServer(protocol=AudioCookieProtocol, port=1500).run()

On Linux client:
    > netcat <server ip> 1500 | aplay -
    

How does it work?
-----------------

AudioCookieProtocol creates a ReadFileAdapter and configures it to read the
standard output result of running the afortune.pl script, at a fixed rate of
95.2kbit/s.

afortune.pl randomly selects a file and returns its contents.

The ReadFileAdapter's "outbox" outbox is directly wired to pass through to the
"outbox" outbox of AudioCookieProtocol.

This component does not terminate.

No EOF/termination indication is given once the end of the file is reached.

"""
import sys
from Axon.Component import component
from Axon.Ipc import newComponent
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor

class AudioCookieProtocol(component):
    """   AudioCookieProtocol([debug]) -> new AudioCookieProtocol component.

   A protocol that spits out raw audio data from a randomly selected audio file.

   Keyword arguments:
   
   - debug  -- Debugging output control (default=0)
   """
    Inboxes = {'inbox': 'NOT USED', 'control': 'NOT USED'}
    Outboxes = {'outbox': 'Raw audio data', 'signal': 'producerFinished() at end of data'}

    def __init__(self, debug=0):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(AudioCookieProtocol, self).__init__()
        self.debug = debug

    def initialiseComponent(self):
        """      Initialises component. Sets up a ReadFileAdapter to read in the contents
      of an audio file at 95.2kbit/s and wires it to fire the contents out
      """
        myDataSource = ReadFileAdaptor(command='./afortune.pl', readmode='bitrate', bitrate=95200, chunkrate=25)
        assert self.debugger.note('AudioCookieProtocol.initialiseComponent', 1, 'Initialising AudioCookieProtocol protocol handler ', self.name)
        self.link(source=(myDataSource, 'outbox'), sink=(
         self, 'outbox'), passthrough=2)
        self.addChildren(myDataSource)
        return newComponent(myDataSource)

    def mainBody(self):
        """Main body - sits and waits, as ReadFileAdapter is getting on with the work for us"""
        return 1


__kamaelia_components__ = (
 AudioCookieProtocol,)
if __name__ == '__main__':
    from Kamaelia.Chassis.ConnectedServer import SimpleServer
    SimpleServer(protocol=AudioCookieProtocol, port=1500).run()