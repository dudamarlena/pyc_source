# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/proxylet/streams.py
# Compiled at: 2009-03-17 20:08:36
"""

  proxylet.streams:  various stream wrappers for proxylet

We utilize a very small portion of the filelike API  to implement streams,
just readline() and the iterator built on it, write() and close().

Some useful classes include HTTPRequest, HTTPResponse, HTTPRewriter and
XMLRewriter.

"""
from paste import httpheaders as hdr
from xml.parsers import expat
from eventlet.greenio import GreenFile

class StreamWrapper(object):
    """Base class for wrapping of streams."""

    def __init__(self, stream):
        if not hasattr(stream, 'readline') and hasattr(stream, 'recv'):
            stream = GreenFile(stream)
        self.stream = stream

    def readline(self, size=None):
        return self.stream.readline(size)

    def __iter__(self):
        ln = self.readline()
        while ln != '':
            yield ln
            ln = self.readline()

    def write(self, data):
        return self.stream.write(data)

    def close(self):
        self.stream.close()


class Nullify(StreamWrapper):
    """/dev/null equivalent for streams."""

    def readline(self, size=None):
        for ln in self.stream:
            pass

        return ''

    def write(self, data):
        pass


class StringStream(StreamWrapper):
    """Stream giving contents of a string."""

    def write(self, data):
        raise RuntimeError('StringStream cannot be written')

    def close(self, data):
        raise RuntimeError('StringStream cannot be closed')

    def readline(self, size=None):
        idx = self.stream.find('\n')
        if idx < 0:
            idx = len(self.stream)
        else:
            idx += 1
        if size is not None and idx > size:
            idx = size
        out = self.stream[:idx]
        self.stream = self.stream[idx:]
        return out


class CallOnClose(StreamWrapper):
    """Invoke a callback when reading from a stream has finished."""

    def __init__(self, stream, onclose):
        StreamWrapper.__init__(self, stream)
        self.onclose = onclose

    def readline(self, size=None):
        ln = self.stream.readline(size)
        if ln == '':
            self.onclose()
        return ln


class ReadNBytes(StreamWrapper):
    """Read up to N bytes from the stream."""

    def __init__(self, stream, nbytes):
        self.nbytes = nbytes
        StreamWrapper.__init__(self, stream)

    def readline(self, size=None):
        if self.nbytes == 0:
            return ''
        if size is None or size > self.nbytes:
            size = self.nbytes
        ln = self.stream.readline(size)
        self.nbytes = self.nbytes - len(ln)
        return ln


class HTTPStream(StreamWrapper):
    """Wrapper for reading a single http request/response from a stream.
    Call parse() to read the headers from the stream into the "headers"
    attribute, which can be manipulated using the paste.httpheaders module.
    """

    def __init__(self, stream):
        StreamWrapper.__init__(self, stream)
        self.headers = []
        self._lines = self._generateLines()

    def parse(self):
        self._headline = self.stream.readline()
        self.parseHeaders()
        self.body = self._generateBody()

    def parseHeaders(self):
        for ln in self.stream:
            if ln.isspace():
                self._sepline = ln
                break
            self.parseHeader(ln)

    def parseHeader(self, ln):
        bits = ln.split(':')
        name = bits[0]
        value = (':').join(bits[1:])[1:].strip()
        self.headers.append((name, value))

    def _generateLines(self):
        if not hasattr(self, 'body'):
            self.parse()
        yield self._headline
        for (name, value) in self.headers:
            yield name + ': ' + value + '\r\n'

        yield self._sepline
        for ln in self.body:
            yield ln

    def _generateBody(self):
        cl = self._getContentLength()
        if cl is None:
            stream = self.stream
        else:
            stream = ReadNBytes(self.stream, int(cl))
        for ln in stream:
            yield ln

        return

    def _getContentLength(self):
        cl = hdr.CONTENT_LENGTH(self.headers)
        if cl == '':
            cl = None
        return cl

    def readline(self, size=None):
        try:
            return self._lines.next()
        except StopIteration:
            return ''


class HTTPRequest(HTTPStream):
    """Read a single HTTP request from the stream.
    The entire request header will be read and made available
    in the following attributes:

        * reqURI:     the requested URI
        * reqMethod:  the request method
        * headers:    the HTTP headers, as a list of (name,value) pairs

    If the request is invalid, then the attribute 'valid' will be
    set to false and no more of the stream is read.
    """

    def __init__(self, stream):
        HTTPStream.__init__(self, stream)
        self.valid = True
        self.parse()
        self.parseReqLine()
        if hdr.HOST(self.headers) is None:
            self.valid = False
        if not self.valid:
            self._lines = Nullify(self.stream)
        return

    def parseReqLine(self):
        bits = self._headline.split()
        if len(bits) != 3:
            self.valid = False
            return
        self.reqMethod = bits[0]
        self.reqURI = bits[1]
        self.reqProtocol = bits[2]

    def _generateLines(self):
        lines = HTTPStream._generateLines(self)
        lines.next()
        yield (' ').join((self.reqMethod, self.reqURI, self.reqProtocol)) + '\r\n'
        for ln in lines:
            yield ln

    def _getContentLength(self):
        cl = HTTPStream._getContentLength(self)
        if cl is None:
            if not hdr.TRANSFER_ENCODING(self.headers):
                cl = 0
        return cl


class HTTPResponse(HTTPStream):
    """Read a single HTTP response from the stream."""
    pass


class HTTPRewriter(StreamWrapper):
    """Rewrite a HTTP stream.

    Subclasses should implement one or both of the methods 'rwHeaders'
    and 'rwBody', which will be invoked at the appropriate times.

    Special care is taken to keep the content-length header accurate,
    if it is present.  This may mean that the entire body must be read
    before any can be output.
    """

    def __init__(self, stream):
        StreamWrapper.__init__(self, stream)
        self._lines = self._generateLines()

    def readline(self, size=None):
        try:
            return self._lines.next()
        except StopIteration:
            return ''

    def _generateLines(self):
        if not hasattr(self.stream, 'body'):
            self.stream.parse()
        if hasattr(self, 'rwHeaders'):
            self.rwHeaders(self.stream.headers)
        yield self.stream.readline()
        hasCL = hdr.CONTENT_LENGTH(self.stream.headers)
        hasCL = hasCL not in (None, '', '0')
        if hasattr(self, 'rwBody'):
            self.stream.body = self.rwBody(self.stream.body)
            if hasCL:
                body = []
                newCL = 0
                for ln in self.stream.body:
                    body.append(ln)
                    newCL += len(ln)

                self.stream.body = body
                hdr.CONTENT_LENGTH.update(self.stream.headers, newCL)
        for ln in self.stream:
            yield ln

        return


class XMLRewriter(StreamWrapper):
    """Rewrite a stream containing XML.

    This class is used to read from a stream yielding chunks of
    XML content, apply some transformations to the data, and send
    the new XML out as a stream
 
    It supports only a single rewriting function self.rewrite. To
    indicate what parts of the document to rewrite, set entries
    corresponding to tag names in self.rw_content{} and entries
    corresponding to tag and attribute names in self.rw_attrs.
    Example:

        rw = XMLRewriter(stream)
        rw.rewrite = rewrite_func
        rw.rw_content["element1"] = True
        rw.rw_attrs["element2"] = {"attr1": True, "attr2": True}
        for ln in rw:
          do_something(ln)

    Note that we don't do any fancy processing of XML namespaces
    or things like that - very basic processing only.  Maybe in
    the next version...
    """

    def __init__(self, stream):
        StreamWrapper.__init__(self, stream)
        self._output = []
        self.rw_content = {}
        self.rw_attrs = {}
        self._content = None
        self._lines = self._generateLines()
        return

    def readline(self, size=None):
        try:
            return self._lines.next()
        except StopIteration:
            return ''

    def _generateLines(self):
        parser = expat.ParserCreate()
        parser.XmlDeclHandler = self.XmlDecl
        parser.StartElementHandler = self.StartElement
        parser.EndElementHandler = self.EndElement
        parser.CharacterDataHandler = self.CharacterData
        for chunk in self.stream:
            parser.Parse(chunk)
            for result in self._output:
                yield result

            self._output = []

        parser.Parse('', True)
        for result in self._output:
            yield result

    def XmlDecl(self, version, encoding, standalone):
        self._output.append('<?xml version="')
        self._output.append(str(version))
        if encoding is not None:
            self._output.append('" encoding="')
            self._output.append(str(encoding))
        self._output.append('"?>')
        return

    def StartElement(self, name, attributes):
        if self.rw_content.get(name):
            self._content = ''
        arw = self.rw_attrs.get(name, {})
        for a in arw:
            try:
                val = attributes[a]
                attributes[a] = self.rewrite(val)
            except KeyError:
                pass

        atts = [ '%s="%s"' % (k, v) for (k, v) in attributes.iteritems() ]
        atts = [name] + atts
        self._output.append('<%s>' % ((' ').join(atts),))

    def EndElement(self, name):
        c = self._content
        if c is not None:
            self._content = None
            self.CharacterData(self.rewrite(c))
        self._output.append('</%s>' % (name,))
        return

    def CharacterData(self, data):
        if self._content is not None:
            self._content += data
        else:
            self._output.append(data)
        return