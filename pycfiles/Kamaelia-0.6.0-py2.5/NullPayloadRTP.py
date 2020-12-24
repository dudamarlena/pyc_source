# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/RTP/NullPayloadRTP.py
# Compiled at: 2008-10-19 12:19:52
"""
Null Payload RTP Classes.
Null Payload Pre-Framer.
Null Payload RTP Packet Stuffer - Same thing.

This Null payload also assumes constant bit rate load.

Subcomponents functionality:
    
* FileControl: - Only if RFA internal - isn't
    * FileReader - only if internal - isn't
    * FileSelector - only if internal - isn't
* Format Decoding
* DataFramaing
* Command Interpreter (Likely to be component core code)
"""
from Axon.Component import component, scheduler, newComponent

def packLengthAsString(aNumber):
    r1, r2, byte1 = aNumber >> 8, aNumber >> 16, aNumber >> 24
    byte2 = r2 - (byte1 << 8)
    byte3 = r1 - (r2 << 8)
    byte4 = aNumber - (r1 << 8)
    return ('').join([ chr(x) for x in [byte1, byte2, byte3, byte4] ])


class NullPayloadPreFramer(component):
    """
   Inboxes:
       control -> File select, file read control, framing control
       recvsrc -> Block/Chunks of raw disk data
   Outboxes:
       activatesrc -> Control messages to the file reading subsystem
       output -> The framed data, payload ready
   """
    Inboxes = [
     'control', 'recvsrc']
    Outboxes = ['output']
    Usescomponents = []

    def __init__(self, sourcename, sourcebitrate=65536, chunksize=1400):
        """* Name of source - at __init__
         * Data Rate - at __init__
         * Chunksize - at __init__
      """
        super(NullPayloadPreFramer, self).__init__()
        self.sourcename = sourcename
        self.sourcebitrate = sourcebitrate
        self.sourceoctetrate = sourcebitrate / 8.0
        self.chunksize = chunksize
        self.currentchunk = ''
        self.timestamp = 0
        self._dataSent = 0
        self.quitFlag = False

    def initialiseComponent(self):
        """No initialisation"""
        return 1

    def updateTimestamp(self, datatosend):
        """C.updateTimestamp(datatosend)

      self.timestamp stores the timestamp of the end of the most recently
      transmitted data, whenever we send some data this timestamp needs to
      be updated. This method represents the calculation involved. (calculate
      the time period the data covers, and increment the timestamp)
      """
        self._dataSent += len(datatosend)
        self.timestamp = self._dataSent / self.sourceoctetrate

    def makeChunk(self, datatosend):
        """C.makeChunk(datatosend) -> chunk : network ready data
      """
        lengthToSend = packLengthAsString(len(datatosend))
        chunk = lengthToSend + datatosend
        return chunk

    def sendCurrentChunk(self, sendpartial=False):
        """ * grab first (current chunk size) bytes
          * frame chunk
          * send chunk
      """
        if len(self.currentchunk) < self.chunksize and not sendpartial:
            return 0
        datatosend, self.currentchunk = self.currentchunk[0:self.chunksize], self.currentchunk[self.chunksize:]
        timestamp = self.timestamp
        self.updateTimestamp(datatosend)
        chunk = self.makeChunk(datatosend)
        result = (timestamp, chunk)
        self.send(result, 'output')
        return 1

    def handleShutdown(self):
        if len(self.currentchunk) > 0:
            self.sendCurrentChunk(sendpartial=True)
            return 2
        return 0

    def handleControl(self):
        """returns quit flag - True means quit"""
        if self.dataReady('control'):
            message = self.recv('control')
            if message == 'shutdown':
                return True
        return False

    def mainBody(self):
        """Loopbody:
      """
        if len(self.currentchunk) >= self.chunksize:
            self.sendCurrentChunk()
            return 1
        if self.quitFlag:
            return self.handleShutdown()
        if self.dataReady('recvsrc'):
            self.currentchunk += self.recv('recvsrc')
            return 3
        if self.dataReady('control'):
            self.quitFlag = self.handleControl()
            return 4
        return 5

    def closeDownComponent(self):
        """No closedown/shutdown code"""
        pass


__kamaelia_components__ = (
 NullPayloadPreFramer,)
if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor

    class NullPayloadPreFramer_testHarness(component):

        def __init__(self):
            super(NullPayloadPreFramer_testHarness, self).__init__()
            self.source = ReadFileAdaptor('Support/BlankFile.txt', readsize='1450', steptime=0)
            self.transform = NullPayloadPreFramer('TestSource', 65536, chunksize=257)
            self.sink = ConsoleEchoer()

        def initialiseComponent(self):
            self.link((self.source, 'outbox'), (self.transform, 'recvsrc'))
            self.link((self.transform, 'output'), (self.sink, 'inbox'))
            return newComponent(self.source, self.transform, self.sink)

        def mainBody(self):
            """The system will run until it hits a dead end, and then spin"""
            return 1


    NullPayloadPreFramer_testHarness().activate()
    scheduler.run.runThreads()