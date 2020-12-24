# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted_goodies/simpleserver/http/wsgi.py
# Compiled at: 2007-08-03 10:13:28
"""
A non-blocking container resource for WSGI web applications.
"""
import os, threading, sys, Queue
from zope.interface import implements
from twisted.internet import defer, interfaces, reactor
from twisted.python import log, failure
from twisted.web2 import http, http_headers
from twisted.web2 import iweb, server, stream, resource
from twisted.web2.twcgi import createCGIEnvironment
from asynqueue import ThreadQueue
VERBOSE = False
MAX_PENDING = 10
IP_BAN_SECS = 30.0

class AlreadyStartedResponse(Exception):
    __module__ = __name__


class WSGIMeta(type):
    """
    """
    __module__ = __name__

    def __new__(mcls, name, bases, dictionary):
        if not hasattr(mcls, 'globalStuff'):
            gs = mcls.globalStuff = {}
            gs['queue'] = ThreadQueue(1)
            gs['pending'] = 0
            gs['handlers'] = []
            gs['banned'] = {}
        for (name, value) in mcls.globalStuff.iteritems():
            dictionary[name] = value

        newClass = super(WSGIMeta, mcls).__new__(mcls, name, bases, dictionary)
        return newClass


class TracerMixin(object):
    """
    Mix me in to trace problems
    """
    __module__ = __name__
    isTracing = False
    traceFrame = None
    traceStack = [('cache.py', 'get_changes'), ('changeset.py', 'get_changes'), ('changeset.py', '_render_html')]
    traceLevels = 5

    def settrace(self):
        """
        Call this method to start tracing. If you're using threads, you must
        call it within the same thread whose execution you want to trace.
        """
        sys.settrace(self.trace)
        self.isTracing = True

    def trace(self, frame, event, arg):
        """
        This is the actual trace function.
        """

        def msg(level):
            values = [
             '.' * level]
            values.extend([ getattr(frame.f_code, 'co_%s' % x) for x in ('filename',
                                                                         'firstlineno',
                                                                         'name') ])
            if values != getattr(self, '_prevMsgValues', None):
                self._prevMsgValues = values
                print '%s %s (%04d): %s' % tuple(values)
            return

        def isTraceEntry(k, thisFrame):
            if thisFrame.f_code.co_name == self.traceStack[k][1]:
                tail = '/%s' % self.traceStack[k][0]
                if thisFrame.f_code.co_filename.endswith(tail):
                    return True

        def frameGenerator(N):
            nextFrame = frame
            for k in xrange(N):
                yield (
                 k, nextFrame)
                nextFrame = nextFrame.f_back

        if not self.isTracing:
            return
        if event == 'call':
            level = 1
            if self.traceFrame is None:
                N = len(self.traceStack)
                for (k, thisFrame) in frameGenerator(N):
                    if not isTraceEntry(k, thisFrame):
                        return
                else:
                    print '-' * 40
                    self.traceFrame = frame
            for (k, thisFrame) in frameGenerator(self.traceLevels):
                level += 1
                if thisFrame in (None, self.traceFrame):
                    break
            else:
                return

            msg(level)
            return self.trace
        elif event == 'return' and frame == self.traceFrame:
            self.traceFrame = None
            print '->', arg
        return


class WSGIResource(TracerMixin, object):
    """
    A web2 Resource which wraps the given WSGI application callable.

    The WSGI application will be called in a separate thread (using
    the reactor threadpool) whenever a request for this resource or
    any lower part of the url hierarchy is received.

    This isn't a subclass of resource.Resource, because it shouldn't do any
    method-specific actions at all. All that stuff is totally up to the
    contained wsgi application
    """
    __module__ = __name__
    __metaclass__ = WSGIMeta
    implements(iweb.IResource, interfaces.IFinishableConsumer)

    def __init__(self, application):
        self.application = application
        self.queue.subscribe(self)

    def renderHTTP(self, req):

        def done(result, IP):
            if not result or isinstance(result, failure.Failure):
                if VERBOSE:
                    print 'Failed request from %s' % IP
                self.banIP(IP)
            if handler in self.handlers:
                self.handlers.remove(handler)

        IP = req.remoteAddr.host
        if IP in self.banned:
            return self.denial()
        handler = WSGIHandler(self.application, req)
        self.handlers.append(handler)
        if self.isTracing:
            d = defer.succeed(None)
        else:
            d = self.queue.call(self.settrace)
        d.addCallback(lambda _: self.queue.call(handler.run))
        d.addBoth(done, IP)
        return handler.responseDeferred

    def banIP(self, IP):
        """
        Temporarily bans the specified IP address from making connections.
        """
        if IP in self.banned:
            (d, delayedCall) = self.banned[IP]
            delayedCall.cancel()
            d.callback(IP)
        d = defer.Deferred()
        d.addCallback(self.banned.pop)
        delayedCall = reactor.callLater(IP_BAN_SECS, d.callback, IP)
        self.banned[IP] = (d, delayedCall)

    def denial(self):
        title = 'Access Denied'
        html = '<html>'
        html += '<head><title>%s</title></head>' % title
        html += '<body>'
        html += '<h1>%s</h1>' % title
        html += '<p>Access from your IP has been temporarily denied</p>'
        html += '</body></html>'
        return http.Response(200, {'content-type': http_headers.MimeType('text', 'html')}, html)

    def locateChild(self, request, segments):
        return (
         self, server.StopTraversal)

    def registerProducer(self, producer, streaming):
        pass

    def unregisterProducer(self):
        pass

    @classmethod
    def write(cls, new):
        old = cls.pending
        cls.pending = new
        if VERBOSE and new != old:
            print 'Pending: %02d -> %02d' % (old, new)
        if new > MAX_PENDING and cls.handlers:
            if new > min([old, 2 * MAX_PENDING]):
                oldestHandler = cls.handlers.pop(0)
                if VERBOSE:
                    print 'Stopping handler:', oldestHandler
                oldestHandler.stopProducing()

    def finish(self):
        while self.handlers:
            handler = self.handlers.pop(0)
            handler.inputStream.close()

        del self.application


class FinishableBufferedStream(stream.BufferedStream):
    """
    """
    __module__ = __name__

    def __init__(self, stream):
        self.running = True
        super(FinishableBufferedStream, self).__init__(stream)

    def _readUntil(self, f):
        """
        Non-borked internal helper function which repeatedly calls f each
        time after more data has been received, until it returns non-None.
        """
        while self.running:
            r = f()
            if r is not None:
                yield r
                return
            newdata = self.stream.read()
            if isinstance(newdata, defer.Deferred):
                newdata = defer.waitForDeferred(newdata)
                yield newdata
                newdata = newdata.getResult()
            if newdata is None:
                newdata = self.data
                self.data = ''
                yield newdata
                return
            self.data += str(newdata)

        return

    _readUntil = defer.deferredGenerator(_readUntil)

    def finish(self):
        self.stream.finish()
        self.running = False


class InputStream(object):
    """
    This class implements the 'wsgi.input' object. The methods are
    expected to have the same behavior as the same-named methods for
    python's builtin file object.
    """
    __module__ = __name__

    def __init__(self, newstream):
        self.stream = FinishableBufferedStream(newstream)

    def callInReactor(self, f, *args, **kw):
        """
        Read a line, delimited by a newline. If the stream reaches EOF
        or size bytes have been read before reaching a newline (if
        size is given), the partial line is returned.

        COMPATIBILITY NOTE: the size argument is excluded from the
        WSGI specification, but is provided here anyhow, because
        useful libraries such as python stdlib's cgi.py assume their
        input file-like-object supports readline with a size
        argument. If you use it, be aware your application may not be
        portable to other conformant WSGI servers.
        """

        def call(queue):
            result = defer.maybeDeferred(f, *args, **kw)
            result.addBoth(queue.put)

        from twisted.internet import reactor
        queue = Queue.Queue()
        reactor.callFromThread(call, queue)
        result = queue.get()
        if isinstance(result, failure.Failure):
            result.raiseException()
        return result

    def read(self, size=None):
        """
        Read at most size bytes from the input, or less if EOF is
        encountered. If size is ommitted or negative, read until EOF.
        """
        if size < 0:
            size = None
        result = self.callInReactor(self.stream.readExactly, size)
        return result

    def readline(self):
        line = self.callInReactor(self.stream.readline, '\n')
        if line is not None:
            line += '\n'
        return line

    def readlines(self, hint=None):
        """
        Read until EOF, collecting all lines in a list, and returns
        that list. The hint argument is ignored (as is allowed in the
        API specification)
        """
        data = self.read()
        lines = data.split('\n')
        last = lines.pop()
        lines = [ s + '\n' for s in lines ]
        if last != '':
            lines.append(last)
        return lines

    def finish(self):
        """
        Call this if this input stream is backing things up too much.
        """
        if VERBOSE:
            print 'Closing laggard input stream...'
        self.stream.finish()

    def __iter__(self):
        """
        Returns an iterator, each iteration of which returns the
        result of readline(), and stops when readline() returns an
        empty string.
        """
        while True:
            line = self.readline()
            if not line:
                return
            yield line


class ErrorStream(object):
    """
    This class implements the 'wsgi.error' object.
    """
    __module__ = __name__

    def flush(self):
        pass

    def write(self, s):
        log.msg('WSGI app error: ' + s, isError=True)

    def writelines(self, seq):
        s = ('').join(seq)
        log.msg('WSGI app error: ' + s, isError=True)


class WSGIHandler(object):
    """
    """
    __module__ = __name__
    implements(interfaces.IPushProducer)
    headersSent = False
    stream = None

    def __init__(self, application, request):
        self.setupEnvironment(request)
        self.application = application
        self.request = request
        self.response = None
        self.responseDeferred = defer.Deferred()
        return

    def setupEnvironment(self, request):
        """
        """
        self.inputStream = InputStream(request.stream)
        env = createCGIEnvironment(request)
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = env['REQUEST_SCHEME']
        env['wsgi.input'] = self.inputStream
        env['wsgi.errors'] = ErrorStream()
        env['wsgi.multithread'] = True
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        env['wsgi.file_wrapper'] = FileWrapper
        self.environment = env

    def startWSGIResponse(self, status, response_headers, exc_info=None):
        """
        """
        if exc_info is not None:
            try:
                if self.headersSent:
                    raise exc_info[0], exc_info[1], exc_info[2]
            finally:
                exc_info = None
        elif self.response is not None:
            raise AlreadyStartedResponse, 'startWSGIResponse(%r)' % status
        status = int(status.split(' ')[0])
        self.response = http.Response(status)
        for (key, value) in response_headers:
            self.response.headers.addRawHeader(key, value)

        return self.write

    def run(self):
        """
        """
        self.ok = True
        from twisted.internet import reactor
        try:
            result = self.application(self.environment, self.startWSGIResponse)
            self.handleResult(result)
        except:
            if not self.headersSent:
                reactor.callFromThread(self.__error, failure.Failure())
            else:
                reactor.callFromThread(self.stream.finish, failure.Failure())

        return self.ok

    def __callback(self):
        self.responseDeferred.callback(self.response)
        self.responseDeferred = None
        return

    def __error(self, f):
        self.responseDeferred.errback(f)
        self.responseDeferred = None
        return

    def write(self, output):
        from twisted.internet import reactor
        if self.response is None:
            raise RuntimeError("Application didn't call startResponse before writing data!")
        if not self.headersSent:
            self.stream = self.response.stream = stream.ProducerStream()
            self.headersSent = True
            self.unpaused = threading.Event()

            def _start():
                self.stream.registerProducer(self, True)
                self.__callback()
                self.unpaused.set()

            reactor.callFromThread(_start)
        self.unpaused.wait()
        reactor.callFromThread(self.stream.write, output)
        return

    def writeAll(self, result):
        from twisted.internet import reactor
        if not self.headersSent:
            if self.response is None:
                raise RuntimeError("Application didn't call startResponse before " + 'writing data!')
            length = 0
            for item in result:
                length += len(item)

            self.response.stream = stream.ProducerStream(length=length)
            self.response.stream.buffer = list(result)
            self.response.stream.finish()
            reactor.callFromThread(self.__callback)
        else:

            def _write():
                for s in result:
                    self.stream.write(s)

                self.stream.finish()

            reactor.callFromThread(_write)
        return

    def handleResult(self, result):
        try:
            from twisted.internet import reactor
            if isinstance(result, FileWrapper):
                if hasattr(result.filelike, 'fileno') and not self.headersSent:
                    if self.response is None:
                        raise RuntimeError("Application didn't call startResponse before " + 'writing data!')
                    self.headersSent = True
                    self.response.stream = stream.FileStream(os.fdopen(os.dup(result.filelike.fileno())))
                    reactor.callFromThread(self.__callback)
                    return
                if type(result) in (list, tuple):
                    self.writeAll(result)
                    return
                for data in result:
                    self.write(data)

                if self.headersSent or self.response is None:
                    raise RuntimeError("Application didn't call startResponse, and didn't " + 'send any data!')
                self.headersSent = True
                reactor.callFromThread(self.__callback)
            else:
                reactor.callFromThread(self.stream.finish)
        finally:
            if hasattr(result, 'close'):
                result.close()
        return

    def pauseProducing(self):
        self.unpaused.set()

    def resumeProducing(self):
        self.unpaused.clear()

    def stopProducing(self):
        """
        Call this if this WSGI call is backing things up too much or has some
        other connection problem that causes it to terminate prematurely.
        """
        self.ok = False
        if self.inputStream:
            self.inputStream.finish()
        if self.stream:
            self.stream.finish()


class FileWrapper(object):
    """
    Wrapper to convert file-like objects to iterables, to implement
    the optional 'wsgi.file_wrapper' object.
    """
    __module__ = __name__

    def __init__(self, filelike, blksize=8192):
        self.filelike = filelike
        self.blksize = blksize
        if hasattr(filelike, 'close'):
            self.close = filelike.close

    def __iter__(self):
        return self

    def next(self):
        data = self.filelike.read(self.blksize)
        if data:
            return data
        raise StopIteration


__all__ = [
 'WSGIResource']