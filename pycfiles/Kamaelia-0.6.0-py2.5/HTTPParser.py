# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/HTTP/HTTPParser.py
# Compiled at: 2008-10-19 12:19:52
"""===========
HTTP Parser
===========

This component is for transforming HTTP requests or responses
into multiple easy-to-use dictionary objects.

Unless you are implementing a new HTTP component you should not
use this component directly. Either SimpleHTTPClient, HTTPServer (in
conjuncton with SimpleServer) or SingleShotHTTPClient will
likely serve your needs.

If you want to use it directly, note that it doesn't output strings
but ParsedHTTPHeader, ParsedHTTPBodyChunk and ParsedHTTPEnd objects.

Example Usage
-------------

If you want to play around with parsing HTTP responses: (like a client)::

    pipeline(
        ConsoleReader(),
        HTTPParser(mode="response"),
        ConsoleEchoer()
    ).run()

If you want to play around with parsing HTTP requests: (like a server)::

    pipeline(
        ConsoleReader(),
        HTTPParser(mode="response"),
        ConsoleEchoer()
    ).run()

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
import string

def splitUri(url):
    requestobject = {'raw-uri': url, 'uri-protocol': '', 'uri-server': ''}
    splituri = string.split(requestobject['raw-uri'], '://')
    if len(splituri) > 1:
        requestobject['uri-protocol'] = splituri[0]
        requestobject['raw-uri'] = requestobject['raw-uri'][len(splituri[0] + '://'):]
    splituri = string.split(requestobject['raw-uri'], '/')
    if splituri[0] != '':
        requestobject['uri-server'] = splituri[0]
        requestobject['raw-uri'] = requestobject['raw-uri'][len(splituri[0]):]
        if requestobject['raw-uri'] == '':
            requestobject['raw-uri'] = '/'
    elif requestobject['uri-protocol'] != '':
        requestobject['uri-server'] = requestobject['raw-uri']
        requestobject['raw-uri'] = '/'
    else:
        requestobject['uri-server'] = ''
    splituri = string.split(requestobject['uri-server'], ':')
    if len(splituri) == 2:
        requestobject['uri-port'] = splituri[1]
        requestobject['uri-server'] = splituri[0]
    splituri = string.split(requestobject['uri-server'], '@')
    if len(splituri) == 2:
        requestobject['uri-username'] = splituri[0]
        requestobject['uri-server'] = requestobject['uri-server'][len(splituri[0] + '@'):]
        splituri = string.split(requestobject['uri-username'], ':')
        if len(splituri) == 2:
            requestobject['uri-username'] = splituri[0]
            requestobject['uri-password'] = splituri[1]
    return requestobject


def removeTrailingCr(line):
    if len(line) == 0:
        return line
    elif line[(-1)] == '\r':
        return line[0:-1]
    else:
        return line


class ParsedHTTPHeader(object):

    def __init__(self, header):
        self.header = header


class ParsedHTTPBodyChunk(object):

    def __init__(self, bodychunk):
        self.bodychunk = bodychunk


class ParsedHTTPEnd(object):
    pass


from Axon.Ipc import WaitComplete

class HTTPParser(component):
    """Component that transforms HTTP requests or responses from a
    single TCP connection into multiple easy-to-use dictionary objects."""
    Inboxes = {'inbox': 'Raw HTTP requests/responses', 
       'control': 'UNUSED'}
    Outboxes = {'outbox': 'HTTP request object', 
       'debug': 'Debugging information', 
       'signal': 'UNUSED'}
    peer = '*** UNDEFINED ***'
    peerport = 0
    localip = '*** UNDEFINED ***'
    localport = 8080

    def __init__(self, mode='request', **argd):
        super(HTTPParser, self).__init__(**argd)
        self.mode = mode
        self.lines = []
        self.readbuffer = ''
        self.currentline = ''
        self.bodiedrequest = False
        self.full_message_sent = False

    def splitProtocolVersion(self, protvers, requestobject):
        protvers = protvers.split('/')
        if len(protvers) != 2:
            requestobject['protocol'] = protvers[0]
            requestobject['version'] = '0'
        else:
            requestobject['protocol'] = protvers[0]
            requestobject['version'] = protvers[1]

    def dataFetch(self):
        """Read once from inbox (generally a TCP connection) and add
        what is received to the readbuffer. This is somewhat inefficient for long lines maybe O(n^2)"""
        if self.dataReady('inbox'):
            self.readbuffer += self.recv('inbox')
            return 1
        else:
            return 0

    def debug(self, msg):
        self.send(msg, 'debug')

    def shouldShutdown(self):
        while self.dataReady('control'):
            temp = self.recv('control')
            if isinstance(temp, shutdown):
                self.debug('HTTPParser should shutdown')
                return True
            elif isinstance(temp, producerFinished):
                self.full_message_sent = True

        return False

    def nextLine(self):
        """Fetch the next complete line in the readbuffer, if there is one"""
        lineendpos = string.find(self.readbuffer, '\n')
        if lineendpos == -1:
            return
        else:
            line = removeTrailingCr(self.readbuffer[:lineendpos])
            self.readbuffer = self.readbuffer[lineendpos + 1:]
            self.debug('Fetched line: ' + line)
            return line
        return

    def handle_requestline(self, splitline, requestobject):
        if len(splitline) < 2:
            requestobject['bad'] = True
        elif len(splitline) == 2:
            requestobject['method'] = splitline[0]
            requestobject['raw-uri'] = splitline[1]
            requestobject['protocol'] = 'HTTP'
            requestobject['version'] = '0.9'
        else:
            requestobject['method'] = splitline[0]
            requestobject.update(splitUri(string.join(splitline[1:-1], '%20')))
            self.splitProtocolVersion(splitline[(-1)], requestobject)

    def getInitialLine(self):
        self.debug('HTTPParser::main - awaiting initial line')
        currentline = None
        while currentline == None:
            self.debug('HTTPParser::main - stage 1')
            if self.shouldShutdown():
                return
            while self.dataFetch():
                pass

            currentline = self.nextLine()
            if currentline == None:
                self.pause()
                yield 1

        self.currentline = currentline
        return

    def getHeaders(self, requestobject):
        previousheader = ''
        endofheaders = False
        while not endofheaders:
            self.debug('HTTPParser::main - stage 2  - Get Headers')
            if self.shouldShutdown():
                return
            while self.dataFetch():
                pass

            currentline = self.nextLine()
            while currentline != None:
                self.debug('HTTPParser::main - stage 2.1')
                if currentline == '':
                    endofheaders = True
                    break
                elif currentline[0] == ' ' or currentline[0] == '\t':
                    requestobject['headers'][previousheader] += ' ' + string.lstrip(currentline)
                else:
                    splitheader = string.split(currentline, ':')
                    requestobject['headers'][string.lower(splitheader[0])] = string.lstrip(currentline[len(splitheader[0]) + 1:])
                currentline = self.nextLine()

            if not endofheaders:
                self.pause()
                yield 1

        self.currentline = currentline
        self.debug('HTTPParser::main - stage 2 complete - Got Headers')
        return

    def getBody_ChunkTransferEncoding(self, requestobject):
        bodylength = -1
        while bodylength != 0:
            self.debug('HTTPParser::main - stage 3.chunked')
            currentline = None
            while currentline == None:
                self.debug('HTTPParser::main - stage 3.chunked.1')
                if self.shouldShutdown():
                    return
                while self.dataFetch():
                    pass

                currentline = self.nextLine()
                if currentline == None:
                    self.pause()
                    yield 1

            splitline = currentline.split(';')
            try:
                bodylength = string.atoi(splitline[0], 16)
            except ValueError:
                bodylength = 0
                requestobject['bad'] = True

            self.debug("HTTPParser::main - chunking: '%s' '%s' %d" % (currentline, splitline, bodylength))
            if bodylength != 0:
                while len(self.readbuffer) < bodylength:
                    self.debug('HTTPParser::main - stage 3.chunked.2')
                    if self.shouldShutdown():
                        return
                    while self.dataFetch():
                        pass

                    if len(self.readbuffer) < bodylength:
                        self.pause()
                        yield 1

                self.send(ParsedHTTPBodyChunk(self.readbuffer[:bodylength]), 'outbox')
            if self.readbuffer[bodylength:bodylength + 2] == '\r\n':
                self.readbuffer = self.readbuffer[bodylength + 2:]
            elif self.readbuffer[bodylength:bodylength + 1] == '\n':
                self.readbuffer = self.readbuffer[bodylength + 1:]
            else:
                requestobject['bad'] = True
                break
            if bodylength == 0:
                break

        self.currentline = currentline
        return

    def getBodyDependingOnHalfClose(self):
        self.debug('HTTPParser::main - stage 3.connection-close start\n')
        connectionopen = True
        while connectionopen:
            if self.shouldShutdown():
                return
            while self.dataFetch():
                pass

            if len(self.readbuffer) > 0:
                self.send(ParsedHTTPBodyChunk(self.readbuffer), 'outbox')
                self.readbuffer = ''
            elif self.full_message_sent:
                connectionopen = False
            while self.dataReady('control'):
                temp = self.recv('control')
                if isinstance(temp, producerFinished):
                    connectionopen = False
                    break
                elif isinstance(temp, shutdown):
                    return

            if connectionopen and not self.anyReady():
                self.pause()
                yield 1

    def getBody_KnownContentLength(self, requestobject):
        if string.lower(requestobject['headers'].get('expect', '')) == '100-continue':
            pass
        self.debug('HTTPParser::main - stage 3.length-known start')
        bodylengthremaining = int(requestobject['headers']['content-length'])
        while bodylengthremaining > 0:
            if self.shouldShutdown():
                return
            while self.dataFetch():
                pass

            if bodylengthremaining < len(self.readbuffer):
                self.send(ParsedHTTPBodyChunk(self.readbuffer[:bodylengthremaining]), 'outbox')
                self.readbuffer = self.readbuffer[bodylengthremaining:]
                bodylengthremaining = 0
            elif len(self.readbuffer) > 0:
                bodylengthremaining -= len(self.readbuffer)
                self.send(ParsedHTTPBodyChunk(self.readbuffer), 'outbox')
                self.readbuffer = ''
            if bodylengthremaining > 0:
                self.pause()
                yield 1

        self.readbuffer = self.readbuffer[bodylengthremaining:]

    def setServer(self, requestobject):
        if requestobject['headers'].has_key('host'):
            requestobject['uri-server'] = requestobject['headers']['host']

    def setConnectionMode(self, requestobject):
        if requestobject['version'] == '1.1':
            requestobject['headers']['connection'] = requestobject['headers'].get('connection', 'keep-alive')
        else:
            requestobject['headers']['connection'] = requestobject['headers'].get('connection', 'close')

    def getBody(self, requestobject):
        self.debug('HTTPParser::main - stage 3 start - Get Post Body')
        if requestobject['headers'].get('transfer-encoding', '').lower() == 'chunked':
            yield WaitComplete(self.getBody_ChunkTransferEncoding(requestobject))
        elif requestobject['headers'].has_key('content-length'):
            yield WaitComplete(self.getBody_KnownContentLength(requestobject))
        else:
            yield WaitComplete(self.getBodyDependingOnHalfClose())
        self.debug('HTTPParser::main - stage 3 end - Got Post Body')

    def initialiseRequestObject(self):
        self.debug('HTTPParser::main - stage 0')
        requestobject = {'bad': False, 'headers': {}, 'version': '0.9', 
           'method': '', 
           'protocol': '', 
           'body': ''}
        if self.mode == 'request':
            requestobject['raw-uri'] = ''
        else:
            requestobject['responsecode'] = ''
        return requestobject

    def handleInitialLine(self, requestobject):
        self.debug('HTTPParser::main - initial line found')
        splitline = string.split(self.currentline, ' ')
        if self.mode == 'request':
            self.handle_requestline(splitline, requestobject)
        elif len(splitline) < 2:
            requestobject['bad'] = True
        else:
            requestobject['responsecode'] = splitline[1]
            self.splitProtocolVersion(splitline[0], requestobject)

    def closeConnection(self):
        self.send(ParsedHTTPEnd(), 'outbox')
        self.debug('HTTPParser connection close\n')
        self.send(producerFinished(self), 'signal')

    def main(self):
        requestobject = self.initialiseRequestObject()
        yield WaitComplete(self.getInitialLine())
        self.handleInitialLine(requestobject)
        if requestobject['bad']:
            self.debug('HTTPParser::main - request line bad\n')
            self.closeConnection()
            return
        if self.mode == 'response' or requestobject['method'] == 'PUT' or requestobject['method'] == 'POST':
            self.bodiedrequest = True
        else:
            self.bodiedrequest = False
        yield WaitComplete(self.getHeaders(requestobject))
        self.setServer(requestobject)
        self.setConnectionMode(requestobject)
        requestobject['peer'] = self.peer
        requestobject['peerport'] = self.peerport
        requestobject['localip'] = self.localip
        requestobject['localport'] = self.localport
        self.send(ParsedHTTPHeader(requestobject), 'outbox')
        if self.bodiedrequest:
            yield WaitComplete(self.getBody(requestobject))
        self.debug('HTTPParser::main - request sent on\n')
        self.closeConnection()
        yield 1


__kamaelia_components__ = (
 HTTPParser,)