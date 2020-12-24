# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted_goodies/webfetch/fetch.py
# Compiled at: 2007-07-25 20:13:09
"""
Fetching of Web pages
"""
import os.path, re
from zope.interface import implements
from twisted.internet import interfaces, reactor, defer, protocol
from twisted.python import failure, procutils
from twisted.web2 import stream as stream_mod
import http

class ImplementationError(Exception):
    """
    There was a problem implementing the required interface.
    """
    __module__ = __name__


class FetchFailure(failure.Failure):
    __module__ = __name__

    class FetchError(Exception):
        __module__ = __name__

    def __init__(self, *explanation):
        e = self.FetchError(*explanation)
        failure.Failure.__init__(self, e)


class SearchConsumer(object):
    """
    I consume HTML from a stream producer until a match is found for
    my regular expression, which is supplied to my constructor as a
    compiled regular expression object.
    """
    __module__ = __name__
    implements(interfaces.IConsumer)

    def __init__(self, regex):
        self.regex = regex

    def registerProducer(self, producer, streaming):
        if not streaming:
            raise TypeError('Only streaming producers are supported')
        self.producer = producer
        self.data = ''

    def unregisterProducer(self):
        if hasattr(self, 'producer'):
            del self.producer

    def write(self, data):
        if not hasattr(self, 'producer'):
            return
        self.m = self.regex.search(data)
        if self.m is None:
            self.data += data
            self.m = self.regex.search(self.data)
            if self.m is None:
                return
        self.producer.stopProducing(None)
        return


class SiteGetterBase(object):
    """
    Construct an instance of one of my subclasses with the I{host} and I{port}
    a web server and you can use it to get, match, or save pages from the
    server.
    """
    __module__ = __name__

    def __init__(self, host, port):
        self.host, self.port = host, port
        self.producers = {}

    def getPage(self, schemePart):
        """
        Gets the web page at my server referenced by the specified URL
        I{schemePart}, returning a deferred that fires with the entire contents
        of the page as a string.
        """

        def gotResponse(response):
            data = []
            d = stream_mod.readStream(response.stream, data.append)
            d.addCallback(lambda _: ('').join(data))
            return d

        return self.connect(schemePart).addCallback(gotResponse)

    def setRegex(self, ID, regex):
        """
        Defines a compiled and internally stored regular expression object
        keyed by the specified integer I{ID} to the supplied pattern string
        I{regex}.
        """
        if not isinstance(ID, int):
            raise TypeError('Regular expression storage keys must be integers')
        if not hasattr(self, 'regexStore'):
            self.regexStore = {}
        self.regexStore[ID] = re.compile(regex)

    def searchPage(self, schemePart, regex):
        """
        Matches the web page at my server referenced by the specified URL
        I{schemePart} against the regular expression I{regex}, returning a
        deferred that fires with a re match object to the first matching text
        of the page or C{None} if no match was found.

        If an integer is supplied as the I{regex}, it will be used as a key
        to retrieve the regex from an internal store of compiled regular
        expression objects, defined via calls to L{setRegex}.

        The deferred fires as soon as a match is found, which can
        improve response time if the text of interest appears near the
        top of the page.
        """

        def gotResponse(response, reObject):
            producer = stream_mod.StreamProducer(response.stream)
            consumer = SearchConsumer(reObject)
            self.producers[producer] = consumer
            d = producer.beginProducing(consumer)
            d.addCallback(lambda _: self.producers.pop(producer).m)
            return d

        self.data = ''
        if isinstance(regex, int):
            reObject = self.regexStore[regex]
        else:
            reObject = re.compile(regex)
        d = self.connect(schemePart)
        d.addCallback(gotResponse, reObject)
        return d

    def savePage(self, schemePart, filePath):
        """
        Saves the web page at my server referenced by the specified URL
        I{schemePart} to the specified I{filePath}, returning a deferred that
        fires when the file has been written.
        """

        def gotResponse(response, fh):
            d = stream_mod.readIntoFile(response.stream, fh)
            d.addCallback(doneReading, fh)
            return d

        def doneReading(result, fh):
            fh.close()
            return result

        fh = open(filePath, 'w')
        d = self.connect(schemePart)
        d.addCallback(gotResponse, fh)
        return d


class TwistedSiteGetter(SiteGetterBase):
    """
    I fetch pages from my designated web server using the L{twisted.web2} HTTP
    client.

    TODO: This still doesn't work with some servers, e.g., the USPTO patent
    image server.
    """
    __module__ = __name__

    def __init__(self, host, port=80):
        SiteGetterBase.__init__(self, host, port)
        self.cc = protocol.ClientCreator(reactor, http.HTTPClientProtocol)

    def shutdown(self):
        """
        Shuts down any connections that are currently open, returning a
        deferred that fires when done.
        """
        return defer.maybeDeferred(self.proto.transport.loseConnection)

    def connect(self, schemePart):
        """
        Connects to my designated web server with an HTTP request for the URL
        whose I{schemePart} is supplied.
        """

        def gotProto(proto):
            print '\nPROTO:', proto
            self.proto = proto
            headers = {'Host': self.host}
            print '\nGET: http://%s:%s%s' % (self.host, self.port, schemePart)
            request = http.http.ClientRequest('GET', schemePart, headers, None)
            d = proto.submitRequest(request, closeAfter=False)
            d.addBoth(gotResponse)
            return d

        def gotResponse(result):
            print 'RESPONSE:', result
            return result

        d = self.cc.connectTCP(self.host, self.port)
        d.addCallback(gotProto)
        return d


class ProcessStream(protocol.ProcessProtocol):
    """
    I am both a process protocol for an external HTTP fetcher such as C{wget}
    and an implementor of the L{twisted.web2} HTTP stream interface.

    All data in a web server's response to an HTTP request is returned through
    an instance of me.
    """
    __module__ = __name__
    implements(stream_mod.IStream)

    def __init__(self):
        self.d_started = defer.Deferred()
        self.d_ended = defer.Deferred()
        self.waiting = []
        self.pending = []
        self.open = True
        self.running = False

    def registerTransport(self, transport):
        """
        Call this method to register the L{interfaces.IProcessTransport}
        provider for my HTTP fetcher process.
        """
        self.transport = transport

    def read(self):
        if self.pending:
            return defer.succeed(self.pending.pop(0))
        elif self.open:
            d = defer.Deferred()
            self.waiting.append(d)
            return d

    def close(self):
        if self.open:
            for d in self.waiting:
                d.callback(None)

            self.open = False
        return

    def connectionMade(self):
        """
        This method is when the HTTP fetcher process has started and is
        ready to produce output, with the following results:
        
            - My 'process started' deferred C{d_started} fires.

            - Any output received from the process after my output stream has
              closed will be ignored and caus the offending process to be
              terminated.
        
        """
        self.running = True
        self.d_started.callback(None)
        return

    def outReceived(self, data):
        """
        This method is called with a chunk of the HTTP response stream from the
        HTTP fetcher process, which it puts into my queue unless my output
        stream has closed, in which case the chunk is ignored and the process
        is terminated.
        """
        if self.waiting:
            self.waiting.pop(0).callback(data)
        elif self.open:
            self.pending.append(data)
        elif self.running:
            try:
                self.transport.signalProcess('HUP')
            except:
                pass

    def outConnectionLost(self):
        """
        This method is called when the HTTP fetcher process is done producing
        output and the HTTP response stream is closed, whereupon I close my own
        output stream.
        """
        self.close()

    def processEnded(self, reason):
        """
        This method is called when the HTTP fetcher process has terminated ,
        whereupon I fire my 'process ended' deferred C{d_ended} once all
        outstanding calls to my L{read} method have been satisfied.
        """
        self.running = False
        d = defer.DeferredList(self.waiting)
        d.chainDeferred(self.d_ended)


class ExternalFetcherResponse(object):
    """
    I represent an HTTP response from a web server.

    @ivar stream: An instance of L{ProcessStream} through which the response
      data can be accessed in an asynchronous fashion.
    
    """
    __module__ = __name__

    def __init__(self, executable, args):
        self.stream = ProcessStream()
        transport = reactor.spawnProcess(self.stream, executable, args=args)
        self.stream.registerTransport(transport)
        self.stream.d_started.addCallback(lambda _: self)


class ExternalSiteGetter(SiteGetterBase):
    """
    I fetch pages from my designated web server using an external process, with
    the HTTP response stream being accessed via an instance of
    L{ProcessStream}.
    """
    __module__ = __name__
    fetcher = 'wget'
    fetcherArgsBase = ['--quiet', '--no-directories', '-O', '-']

    def __init__(self, host, port=80):
        SiteGetterBase.__init__(self, host, port)
        self.executable = procutils.which(self.fetcher)[0]
        if not self.executable:
            raise ImportError("Can't locate %s executable" % self.fetcher)
        self.responses = []

    def shutdown(self):
        """
        Shuts down any connections that are currently open, returning a
        deferred that fires when done.
        """
        dList = [ response.stream.d_ended for response in self.responses ]
        return defer.DeferredList(dList)

    def connect(self, schemePart):
        """
        Connects to my designated web server with an HTTP request for the URL
        whose I{schemePart} is supplied.
        """
        url = 'http://%s:%s%s' % (self.host, self.port, schemePart.strip())
        args = self.fetcherArgsBase + [url]
        response = ExternalFetcherResponse(self.executable, args)
        self.responses.append(response)
        return response.stream.d_started


SiteGetter = ExternalSiteGetter