# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/MimeRequestComponent.py
# Compiled at: 2008-10-19 12:19:52
"""
Mime Request Component.

Takes a request of the form:

XXXXX <url> PROTO/Ver
Key: value
Key: value
Content-Length: value
Key: value
>>blank line<<
>body
text<

And converts it into a python object that contains:
   requestMethod : string
   url : string
   Protocol : string
   Protocol Version : string (not parsed into a number)
   KeyValues : dict
   body : raw data

Has a default inbox, and a default outbox. Requests data comes in the
inbox. MimeRequest objects come out the outbox.
"""
from Axon.Component import component, scheduler, linkage, newComponent
from Axon.Ipc import errorInformation
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Support.Data.MimeObject import mimeObject
import Kamaelia.Support.Data.requestLine

class MimeRequestComponent(component):
    """Component that accepts raw data, parses it into consituent
   parts of a MIME request. Attempts no interpretation of the request
   however.
   """

    def __init__(self):
        super(MimeRequestComponent, self).__init__()
        self.header = {}
        self.requestLineRead = 0
        self.currentLineRead = 0
        self.seenEndHeader = 0
        self.currentLine = ''
        self.currentBytes = ''
        self.requestLine = ''
        self.stillReading = 1
        self.needData = 0
        self.gotRequest = 0
        self.body = ''
        self.step = 0

    def initialiseComponent(self):
        pass

    def nextLine(self):
        if self.dataReady('inbox'):
            theData = self.recv('inbox')
            try:
                self.currentBytes = self.currentBytes + theData
            except TypeError:
                return (0, '')

        try:
            (newline, self.currentBytes) = self.currentBytes.split('\n', 1)
            if newline != '' and newline[(-1)] == '\r':
                newline = newline[0:-1]
            got = 1
        except ValueError:
            return (0, '')

        return (got, newline)

    def getRequestLine(self):
        """Sets the *REQUEST* line arguments"""
        (self.requestLineRead, self.requestLine) = self.nextLine()

    def getALine(self):
        """Sets the *CURRENT* line arguments"""
        (self.currentLineRead, self.currentLine) = self.nextLine()

    def readHeader(self):
        (origkey, value) = self.currentLine.split(': ', 1)
        key = origkey.lower()
        if not self.header.has_key(key):
            self.header[key] = [
             origkey, value]
        else:
            self.header[key][1] = self.header[key][1] + ', ' + value
        self.currentLineRead = 0
        self.currentLine = ''

    def getData(self):
        if self.dataReady('inbox'):
            theData = self.recv('inbox')
            self.currentBytes = self.currentBytes + theData
            self.needData = 0

    def checkEndOfHeader(self):
        if self.currentLine == '' and not self.seenEndHeader:
            self.seenEndHeader = 1
            try:
                self.headerlength = int(self.header['content-length'][1])
            except KeyError:
                self.headerlength = 0
                self.needData = 0

    def handleDataAquisition(self):
        """This is currently clunky and effectively implements a state machine.
      Should consider rewriting as a generator"""
        if not self.requestLineRead:
            self.getRequestLine()
            return 1
        if not self.currentLineRead:
            self.getALine()
            return 2
        self.checkEndOfHeader()
        if not self.seenEndHeader:
            self.readHeader()
            return 3
        self.body = self.body + self.currentBytes
        if not len(self.body) >= self.headerlength:
            if self.needData:
                self.getData()
                return 4
            else:
                self.currentBytes = ''
                self.needData = 1
                return 5

    def mainBody(self):
        if not self.gotRequest:
            if self.handleDataAquisition():
                return 1
        self.gotRequest = 1
        try:
            self.request = Kamaelia.Support.Data.requestLine.requestLine(self.requestLine)
        except Kamaelia.Support.Data.requestLine.BadRequest, br:
            errinf = errorInformation(self, br)
            self.send(errinf, 'signal')
            return 0

        assert self.debugger.note('MimeRequestComponent.mainBody', 5, self.request, '\n')
        assert self.debugger.note('MimeRequestComponent.mainBody', 10, 'HEADER  \t:', self.header)
        assert self.debugger.note('MimeRequestComponent.mainBody', 10, 'BODY    \t:', self.body)
        self.mimeRequest = mimeObject(self.header, self.body, self.request)
        assert self.debugger.note('MimeRequestComponent.mainBody', 5, self.mimeRequest)
        self.send(self.mimeRequest, 'outbox')


__kamaelia_components__ = (
 MimeRequestComponent,)
if __name__ == '__main__':

    class TestHarness(component):

        def main(self):
            reader = ReadFileAdaptor(filename='Support/SampleMIMERequest.txt')
            decoder = MimeRequestComponent()
            self.link((reader, 'outbox'), (decoder, 'inbox'))
            self.link((decoder, 'outbox'), (self, 'inbox'))
            self.addChildren(reader, decoder)
            yield newComponent(*self.children)
            while 1:
                if self.dataReady('inbox'):
                    message = self.recv('inbox')
                    print 'MIME decoded:', repr(message)
                    return
                yield 1


    TestHarness().activate()
    scheduler.run.runThreads()