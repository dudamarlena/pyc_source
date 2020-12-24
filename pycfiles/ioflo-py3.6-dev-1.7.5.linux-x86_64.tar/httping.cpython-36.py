# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aio/http/httping.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 33004 bytes
"""
httping.py  http async io (nonblocking) support

"""
from __future__ import absolute_import, division, print_function
import sys, os
from collections import deque
import codecs, json
if sys.version > '3':
    from urllib.parse import urlsplit, quote, quote_plus, unquote, unquote_plus
else:
    from urlparse import urlsplit
    from urllib import quote, quote_plus, unquote, unquote_plus
try:
    import simplejson as json
except ImportError:
    import json

from ...aid.sixing import *
from ...aid.odicting import odict, lodict, modict
from ...aid import aiding
from ...aid.consoling import getConsole
console = getConsole()
CRLF = b'\r\n'
LF = b'\n'
CR = b'\r'
MAX_LINE_SIZE = 65536
MAX_HEADERS = 100
HTTP_PORT = 80
HTTPS_PORT = 443
HTTP_11_VERSION_STRING = 'HTTP/1.1'
CONTINUE = 100
SWITCHING_PROTOCOLS = 101
PROCESSING = 102
OK = 200
CREATED = 201
ACCEPTED = 202
NON_AUTHORITATIVE_INFORMATION = 203
NO_CONTENT = 204
RESET_CONTENT = 205
PARTIAL_CONTENT = 206
MULTI_STATUS = 207
IM_USED = 226
MULTIPLE_CHOICES = 300
MOVED_PERMANENTLY = 301
FOUND = 302
SEE_OTHER = 303
NOT_MODIFIED = 304
USE_PROXY = 305
TEMPORARY_REDIRECT = 307
BAD_REQUEST = 400
UNAUTHORIZED = 401
PAYMENT_REQUIRED = 402
FORBIDDEN = 403
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
NOT_ACCEPTABLE = 406
PROXY_AUTHENTICATION_REQUIRED = 407
REQUEST_TIMEOUT = 408
CONFLICT = 409
GONE = 410
LENGTH_REQUIRED = 411
PRECONDITION_FAILED = 412
REQUEST_ENTITY_TOO_LARGE = 413
REQUEST_URI_TOO_LONG = 414
UNSUPPORTED_MEDIA_TYPE = 415
REQUESTED_RANGE_NOT_SATISFIABLE = 416
EXPECTATION_FAILED = 417
UNPROCESSABLE_ENTITY = 422
LOCKED = 423
FAILED_DEPENDENCY = 424
UPGRADE_REQUIRED = 426
PRECONDITION_REQUIRED = 428
TOO_MANY_REQUESTS = 429
REQUEST_HEADER_FIELDS_TOO_LARGE = 431
INTERNAL_SERVER_ERROR = 500
NOT_IMPLEMENTED = 501
BAD_GATEWAY = 502
SERVICE_UNAVAILABLE = 503
GATEWAY_TIMEOUT = 504
HTTP_VERSION_NOT_SUPPORTED = 505
INSUFFICIENT_STORAGE = 507
NOT_EXTENDED = 510
NETWORK_AUTHENTICATION_REQUIRED = 511
STATUS_DESCRIPTIONS = {100:'Continue', 
 101:'Switching Protocols', 
 200:'OK', 
 201:'Created', 
 202:'Accepted', 
 203:'Non-Authoritative Information', 
 204:'No Content', 
 205:'Reset Content', 
 206:'Partial Content', 
 300:'Multiple Choices', 
 301:'Moved Permanently', 
 302:'Found', 
 303:'See Other', 
 304:'Not Modified', 
 305:'Use Proxy', 
 306:'(Unused)', 
 307:'Temporary Redirect', 
 400:'Bad Request', 
 401:'Unauthorized', 
 402:'Payment Required', 
 403:'Forbidden', 
 404:'Not Found', 
 405:'Method Not Allowed', 
 406:'Not Acceptable', 
 407:'Proxy Authentication Required', 
 408:'Request Timeout', 
 409:'Conflict', 
 410:'Gone', 
 411:'Length Required', 
 412:'Precondition Failed', 
 413:'Request Entity Too Large', 
 414:'Request-URI Too Long', 
 415:'Unsupported Media Type', 
 416:'Requested Range Not Satisfiable', 
 417:'Expectation Failed', 
 428:'Precondition Required', 
 429:'Too Many Requests', 
 431:'Request Header Fields Too Large', 
 500:'Internal Server Error', 
 501:'Not Implemented', 
 502:'Bad Gateway', 
 503:'Service Unavailable', 
 504:'Gateway Timeout', 
 505:'HTTP Version Not Supported', 
 511:'Network Authentication Required'}
METHODS = ('GET', 'HEAD', 'PUT', 'PATCH', 'POST', 'DELETE', 'OPTIONS', 'TRACE', 'CONNECT')
MAXAMOUNT = 1048576
_MAXLINE = 65536
_MAXHEADERS = 100

class HTTPException(Exception):
    pass


class InvalidURL(HTTPException):
    pass


class UnknownProtocol(HTTPException):

    def __init__(self, version):
        self.args = (
         version,)
        self.version = version


class BadStatusLine(HTTPException):

    def __init__(self, line):
        if not line:
            line = repr(line)
        self.args = (
         line,)
        self.line = line


class BadRequestLine(BadStatusLine):
    pass


class BadMethod(HTTPException):

    def __init__(self, method):
        self.args = (
         method,)
        self.method = method


class LineTooLong(HTTPException):

    def __init__(self, kind):
        HTTPException.__init__(self, 'got more than %d bytes while parsing %s' % (
         MAX_LINE_SIZE, kind))


class PrematureClosure(HTTPException):

    def __init__(self, msg):
        self.args = (
         msg,)
        self.msg = msg


class HTTPError(Exception):
    __doc__ = '\n    HTTP error for use with Valet or Other WSGI servers to raise exceptions\n    caught by the WSGI server.\n\n\n    Attributes:\n        status is int HTTP status code, e.g. 400\n        reason is  str HTTP status text, "Unknown Error"\n        title  is str title of error\n\n        headers is dict of extra headers to add to the response\n        error (int): An internal application error code\n    '
    __slots__ = ('status', 'reason', 'title', 'detail', 'headers', 'fault')

    def __init__(self, status, reason='', title='', detail='', fault=None, headers=None):
        """
        Parameters:
            status is int HTTP status response code
            reason is  str HTTP reason phase for status code
            title is str title of error
            detail is str detailed description of error
            fault is int internal application fault code for tracking
            headers is dict of extra headers to add to the response
        """
        self.status = int(status)
        self.reason = str(reason) if reason else STATUS_DESCRIPTIONS.get(self.status, 'Unknown')
        self.title = title
        self.detail = detail
        self.fault = fault if fault is None else int(fault)
        self.headers = odict(headers) if headers else odict()

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.status)

    def render(self, jsonify=False):
        """
        Render and return the attributes as a bytes
        If jsonify then render as serialized json
        """
        if jsonify:
            data = odict()
            data['status'] = self.status
            data['reason'] = self.reason
            data['title'] = self.title
            data['detail'] = self.detail
            data['fault'] = self.fault
            body = json.dumps(data, indent=2)
        else:
            body = '{} {}\n{}\n{}\n{}'.format(self.status, self.reason, self.title, self.detail, self.fault if self.fault is not None else '')
        return body.encode('iso-8859-1')


def httpDate1123(dt):
    """Return a string representation of a date according to RFC 1123
    (HTTP/1.1).

    The supplied date must be in UTC.
    import datetime
    httpDate1123(datetime.datetime.utcnow())
    'Wed, 30 Sep 2015 14:29:18 GMT'
    """
    weekday = [
     'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][dt.weekday()]
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
     'Oct', 'Nov', 'Dec'][(dt.month - 1)]
    return '%s, %02d %s %04d %02d:%02d:%02d GMT' % (weekday, dt.day, month,
     dt.year, dt.hour, dt.minute, dt.second)


def normalizeHostPort(host, port=None, defaultPort=80):
    """
    Given hostname host which could also be netloc which includes port
    and or port
    generate and return tuple (hostname, port)
    priority is if port is provided in hostname as host:port then use
    otherwise use port otherwise use defaultPort
    """
    if port is None:
        port = defaultPort
    else:
        i = host.rfind(':')
        j = host.rfind(']')
        if i > j:
            if host[i + 1:]:
                port = host[i + 1:]
            host = host[:i]
        if host:
            if host[0] == '[':
                if host[(-1)] == ']':
                    host = host[1:-1]
        try:
            port = int(port)
        except ValueError:
            raise InvalidURL("Nonnumeric port: '{0}'".format(port))

    return (
     host, port)


def parseQuery(query):
    """
    Return odict of parsed query string.
    Utility function
    """
    qargs = odict()
    if ';' in query:
        querySplits = query.split(';')
    else:
        if '&' in query:
            querySplits = query.split('&')
        else:
            querySplits = [
             query]
    for queryPart in querySplits:
        if queryPart:
            if '=' in queryPart:
                key, val = queryPart.split('=', 1)
                val = unquote(val)
            else:
                key = queryPart
                val = 'true'
            qargs[key] = val

    return qargs


def updateQargsQuery(qargs=None, query=''):
    """
    Returns duple of updated (qargs, query)
    Where qargs parameter is odict of query arguments and query parameter is query string
    The returned qargs is updated with query string arguments
    and the returned query string is generated from the updated qargs
    If provided, qargs may have additional fields not in query string
    This allows combining query args from two sources, a dict and a string

    https://www.w3.org/TR/2014/REC-html5-20141028/forms.html#url-encoded-form-data
    """
    if qargs == None:
        qargs = odict()
    if query:
        if ';' in query:
            querySplits = query.split(';')
        else:
            if '&' in query:
                querySplits = query.split('&')
            else:
                querySplits = [
                 query]
        for queryPart in querySplits:
            if queryPart:
                if '=' in queryPart:
                    key, val = queryPart.split('=', 1)
                    val = unquote_plus(val)
                else:
                    key = queryPart
                    val = 'true'
                qargs[key] = val

    qargParts = ['{0}={1}'.format(key, quote_plus(str(val))) for key, val in qargs.items()]
    query = '&'.join(qargParts)
    return (qargs, query)


def unquoteQuery(query):
    """
    Returns query string with unquoted values
    """
    sep = '&'
    parts = []
    if ';' in query:
        splits = query.split(';')
        sep = ';'
    else:
        if '&' in query:
            splits = query.split('&')
        else:
            splits = [
             query]
    for part in splits:
        if part:
            if '=' in part:
                key, val = part.split('=', 1)
                val = unquote_plus(val)
                parts.append('{0}={1}'.format(key, str(val)))
            else:
                key = part
                parts.append[part]

    query = '&'.join(parts)
    return query


def packHeader(name, *values):
    """
    Format and return a header line.

    For example: h.packHeader('Accept', 'text/html')
    """
    if isinstance(name, unicode):
        name = name.encode('ascii')
    name = name.title()
    values = list(values)
    for i, value in enumerate(values):
        if isinstance(value, unicode):
            values[i] = value.encode('iso-8859-1')
        else:
            if isinstance(value, int):
                values[i] = str(value).encode('ascii')

    value = (b', ').join(values)
    return name + b': ' + value


def packChunk(msg):
    """
    Return msg bytes in a chunk
    """
    lines = []
    size = len(msg)
    lines.append('{0:x}\r\n'.format(size).encode('ascii'))
    lines.append(msg)
    lines.append(b'\r\n')
    return (b'').join(lines)


def parseLine(raw, eols=(
 CRLF, LF, CR), kind='event line'):
    """
    Generator to parse  line from raw bytearray
    Each line demarcated by one of eols
    kind is line type string for error message

    Yields None If waiting for more to parse
    Yields line Otherwise

    Consumes parsed portions of raw bytearray

    Raise error if eol not found before MAX_LINE_SIZE
    """
    while True:
        for eol in eols:
            index = raw.find(eol)
            if index >= 0:
                break

        if index < 0:
            if len(raw) > MAX_LINE_SIZE:
                raise LineTooLong(kind)
            else:
                yield
                continue
        if index > MAX_LINE_SIZE:
            raise LineTooLong(kind)
        line = raw[:index]
        index += len(eol)
        del raw[:index]
        yield line


def parseLeader(raw, eols=(
 CRLF, LF), kind='leader header line', headers=None):
    """
    Generator to parse entire leader of header lines from raw bytearray
    Each line demarcated by one of eols
    Yields None If more to parse
    Yields lodict of headers Otherwise as indicated by empty headers

    Raise error if eol not found before  MAX_LINE_SIZE
    """
    headers = headers if headers is not None else lodict()
    while 1:
        for eol in eols:
            index = raw.find(eol)
            if index >= 0:
                break

        if index < 0:
            if len(raw) > MAX_LINE_SIZE:
                raise LineTooLong(kind)
            else:
                yield
                continue
            if index > MAX_LINE_SIZE:
                raise LineTooLong(kind)
            line = raw[:index]
            index += len(eol)
            del raw[:index]
            if line:
                line = line.decode('iso-8859-1')
                key, value = line.split(': ', 1)
                headers[key] = value
            if len(headers) > MAX_HEADERS:
                raise HTTPException('Too many headers, more than {0}'.format(MAX_HEADERS))
            if not line:
                yield headers


def parseChunk(raw):
    """
    Generator to parse next chunk from raw bytearray
    Consumes used portions of raw
    Yields None If waiting for more bytes
    Yields tuple (size, parms, trails, chunk) Otherwise
    Where:
        size is int size of the chunk
        parms is dict of chunk extension parameters
        trails is dict of chunk trailer headers (only on last chunk if any)
        chunk is chunk if any or empty if not

    Chunked-Body   = *chunk
                last-chunk
                trailer
                CRLF
    chunk          = chunk-size [ chunk-extension ] CRLF
                     chunk-data CRLF
    chunk-size     = 1*HEX
    last-chunk     = 1*("0") [ chunk-extension ] CRLF
    chunk-extension= *( ";" chunk-ext-name [ "=" chunk-ext-val ] )
    chunk-ext-name = token
    chunk-ext-val  = token | quoted-string
    chunk-data     = chunk-size(OCTET)
    trailer        = *(entity-header CRLF)
    """
    size = 0
    parms = odict()
    trails = lodict()
    chunk = bytearray()
    lineParser = parseLine(raw=raw, eols=(CRLF,), kind='chunk size line')
    while True:
        line = next(lineParser)
        if line is not None:
            lineParser.close()
            break
        yield

    size, sep, exts = line.partition(b';')
    try:
        size = int(size.strip().decode('ascii'), 16)
    except ValueError:
        raise

    if exts:
        exts = exts.split(b';')
        for ext in exts:
            ext = ext.strip()
            name, sep, value = ext.partition(b'=')
            parms[name.strip()] = value.strip() or None

    if size == 0:
        leaderParser = parseLeader(raw=raw, eols=(
         CRLF, LF),
          kind='trailer header line')
        while True:
            headers = next(leaderParser)
            if headers is not None:
                leaderParser.close()
                break
            yield

        trails.update(headers)
    else:
        while len(raw) < size:
            yield

        chunk = raw[:size]
        del raw[:size]
        lineParser = parseLine(raw=raw, eols=(CRLF,), kind='chunk end line')
        while True:
            line = next(lineParser)
            if line is not None:
                lineParser.close()
                break
            yield

    if line:
        raise ValueError("Chunk end error. Expected empty got '{0}' instead".format(line.decode('iso-8859-1')))
    yield (size, parms, trails, chunk)


def parseBom(raw, bom=codecs.BOM_UTF8):
    """
    Generator to parse bom from raw bytearray
    Yields None If waiting for more to parse
    Yields bom If found
    Yields empty bytearray Otherwise
    Consumes parsed portions of raw bytearray
    """
    size = len(bom)
    while True:
        if len(raw) >= size:
            if raw[:size] == bom:
                del raw[:size]
                yield bom
                break
            yield raw[0:0]
            break
        yield


def parseStatusLine(line):
    """
    Parse the response status line
    """
    line = line.decode('iso-8859-1')
    if not line:
        raise BadStatusLine(line)
    version, status, reason = aiding.repack(3, (line.split()), default='')
    reason = ' '.join(reason)
    if not version.startswith('HTTP/'):
        raise BadStatusLine(line)
    try:
        status = int(status)
        if status < 100 or status > 999:
            raise BadStatusLine(line)
    except ValueError:
        raise BadStatusLine(line)

    return (
     version, status, reason)


def parseRequestLine(line):
    """
    Parse the request start line
    """
    line = line.decode('iso-8859-1')
    if not line:
        raise BadRequestLine(line)
    method, path, version, extra = aiding.repack(4, (line.split()), default='')
    if not version.startswith('HTTP/'):
        raise UnknownProtocol(version)
    if method not in METHODS:
        raise BadMethod(method)
    return (method, path, version)


class EventSource(object):
    __doc__ = '\n    Server Sent Event Stream Client parser\n    '
    Bom = codecs.BOM_UTF8

    def __init__(self, raw=None, events=None, dictable=False):
        """
        Initialize Instance
        raw must be bytearray
        IF events is not None then used passed in deque
            .events will be deque of event odicts
        IF dictable then deserialize event data as json

        """
        self.raw = raw if raw is not None else bytearray()
        self.events = events if events is not None else deque()
        self.dictable = True if dictable else False
        self.parser = None
        self.leid = None
        self.bom = None
        self.retry = None
        self.ended = None
        self.closed = None
        self.makeParser()

    def close(self):
        """
        Assign True to .closed
        """
        self.closed = True

    def parseEvents(self):
        """
        Generator to parse events from .raw bytearray and append to .events
        Each event is odict with the following items:
             id: event id utf-8 decoded or empty
           name: event name utf-8 decoded or empty
           data: event data utf-8 decoded
           json: event data deserialized to odict when applicable pr None

        assigns .retry if any

        Yields None If waiting for more bytes
        Yields True When done

        event         = *( comment / field ) end-of-line
        comment       = colon *any-char end-of-line
        field         = 1*name-char [ colon [ space ] *any-char ] end-of-line
        end-of-line   = ( cr lf / cr / lf / eof )
        eof           = < matches repeatedly at the end of the stream >
        lf            = 
 0xA
        cr            = 
 0xD
        space         = 0x20
        colon         = 0x3A
        bom           = \ufeff when encoded as utf-8 b'ï»¿'
        name-char     = a Unicode character other than LF, CR, or :
        any-char      = a Unicode character other than LF or CR
        Event streams in this format must always be encoded as UTF-8. [RFC3629]
        """
        eid = self.leid
        ename = ''
        edata = ''
        parts = []
        ejson = None
        lineParser = parseLine(raw=(self.raw), eols=(CRLF, LF, CR), kind='event line')
        while 1:
            line = next(lineParser)
            if line is None:
                yield
                continue
            if not line or self.closed:
                if parts:
                    edata = '\n'.join(parts)
                else:
                    if edata:
                        if self.dictable:
                            try:
                                ejson = json.loads(edata, encoding='utf-8', object_pairs_hook=odict)
                            except ValueError as ex:
                                ejson = None
                            else:
                                edata = ejson
                        self.events.append(odict([('id', eid),
                         (
                          'name', ename),
                         (
                          'data', edata)]))
                    if self.closed:
                        lineParser.close()
                        break
                ename = ''
                edata = ''
                parts = []
                ejson = None
                continue
            field, sep, value = line.partition(b':')
            if sep:
                if not field:
                    continue
            field = field.decode('UTF-8')
            if value:
                if value[0:1] == b' ':
                    del value[0]
            value = value.decode('UTF-8')
            if field == 'event':
                ename = value
            else:
                if field == 'data':
                    parts.append(value)
                else:
                    if field == 'id':
                        self.leid = eid = value
                    else:
                        if field == 'retry':
                            try:
                                value = int(value)
                            except ValueError as ex:
                                pass
                            else:
                                self.retry = value

        yield (
         eid, ename, edata)

    def parseEventStream(self):
        """
        Generator to parse event stream from .raw bytearray stream
        appends each event to .events deque.
        assigns .bom if any
        assigns .retry if any
        Parses until connection closed

        Each event is odict with the following items:
              id: event id utf-8 decoded or empty
            name: event name utf-8 decoded or empty
            data: event data utf-8 decoded
            json: event data deserialized to odict when applicable pr None

        Yields None If waiting for more bytes
        Yields True When completed and sets .ended to True
        If BOM present at beginning of event stream then assigns to .bom and
        deletes.
        Consumes bytearray as it parses

        stream        = [ bom ] *event
        event         = *( comment / field ) end-of-line
        comment       = colon *any-char end-of-line
        field         = 1*name-char [ colon [ space ] *any-char ] end-of-line
        end-of-line   = ( cr lf / cr / lf / eof )
        eof           = < matches repeatedly at the end of the stream >
        lf            = 
 0xA
        cr            = 
 0xD
        space         = 0x20
        colon         = 0x3A
        bom           = \ufeff when encoded as utf-8 b'ï»¿'
        name-char     = a Unicode character other than LF, CR, or :
        any-char      = a Unicode character other than LF or CR
        Event streams in this format must always be encoded as UTF-8. [RFC3629]
        """
        self.bom = None
        self.retry = None
        self.leid = None
        self.ended = None
        self.closed = None
        bomParser = parseBom(raw=(self.raw), bom=(self.Bom))
        while True:
            bom = next(bomParser)
            if bom is not None:
                bomParser.close()
                self.bom = bom.decode('UTF-8')
                break
            if self.closed:
                bomParser.close()
                break
            yield

        eventsParser = self.parseEvents()
        while True:
            result = next(eventParser)
            if result is not None:
                eventsParser.close()
                break
            yield

        yield True

    def makeParser(self, raw=None):
        """
        Make event stream parser generator and assign to .parser
        Assign msg to .msg If provided
        """
        if raw:
            self.raw = raw
        self.parser = self.parseEvents()

    def parse(self):
        """
        Service the event stream parsing
        must call .makeParser to setup parser
        When done parsing,
           .parser is None
           .ended is True
        """
        if self.parser:
            result = next(self.parser)
            if result is not None:
                self.parser.close()
                self.parser = None


class Parsent(object):
    __doc__ = '\n    Base class for objects that parse HTTP messages\n    '

    def __init__(self, msg=None, dictable=None, method='GET'):
        """
        Initialize Instance
        msg = bytearray of request msg to parse
        dictable = True If should attempt to convert body to json
        method = method of associated request
        """
        self.msg = msg if msg is not None else bytearray()
        self.dictable = True if dictable else False
        self.parser = None
        self.version = None
        self.length = None
        self.chunked = None
        self.jsoned = None
        self.encoding = 'ISO-8859-1'
        self.persisted = None
        self.started = None
        self.headed = None
        self.bodied = None
        self.ended = None
        self.closed = None
        self.errored = False
        self.error = None
        self.headers = None
        self.parms = None
        self.trails = None
        self.body = bytearray()
        self.text = ''
        self.data = None
        self.method = method.upper() if method else 'GET'
        self.makeParser()

    def reinit(self, msg=None, dictable=None, method='GET'):
        """
        Reinitialize Instance
        msg = bytearray of request msg to parse
        dictable = Boolean flag If True attempt to convert json body
        method = method verb of associated request
        """
        if msg is not None:
            self.msg = msg
        else:
            if dictable is not None:
                self.dictable = True if dictable else False
            if method is not None:
                self.method = method.upper()
        self.data = None

    def close(self):
        """
        Assign True to .closed and close parser
        """
        self.closed = True

    def checkPersisted(self):
        """
        Checks headers to determine if connection should be kept open until
        client closes it
        Sets the .persisted flag
        """
        self.persisted = False

    def parseHead(self):
        """
        Generator to parse headers in heading of .msg
        Yields None if more to parse
        Yields True if done parsing
        """
        if self.headed:
            return
        self.headers = lodict()
        self.checkPersisted()
        self.headed = True
        yield True

    def parseBody(self):
        """
        Parse body
        """
        if self.bodied:
            return
        self.length = 0
        self.bodied = True
        yield True

    def parseMessage(self):
        """
        Generator to parse message bytearray.
        Parses msg if not None
        Otherwise parse .msg
        """
        self.headed = False
        self.bodied = False
        self.ended = False
        self.closed = False
        self.errored = False
        self.error = None
        while not self.started:
            if self.msg:
                self.started = True
                break
            yield

        try:
            headParser = self.parseHead()
            while True:
                result = next(headParser)
                if result is not None:
                    headParser.close()
                    break
                yield

            bodyParser = self.parseBody()
            while True:
                result = next(bodyParser)
                if result is not None:
                    bodyParser.close()
                    break
                yield

        except HTTPException as ex:
            self.errored = True
            self.error = str(ex)

        self.ended = True
        self.started = False
        yield True

    def makeParser(self, msg=None):
        """
        Make message parser generator and assign to .parser
        Assign msg to .msg If provided
        """
        if msg is not None:
            self.msg = msg
        if self.parser:
            self.parser.close()
        self.parser = self.parseMessage()

    def parse(self):
        """
        Service the message parsing
        must call .makeParser to setup parser
        When done parsing,
           .parser is None
           .ended is True
        """
        if self.parser:
            result = next(self.parser)
            if result is not None:
                self.parser.close()
                self.parser = None

    def dictify(self):
        """
        Attempt to convert body to dict data if .dictable or json content-type
        """
        if self.jsoned or self.dictable:
            try:
                self.data = json.loads((self.body.decode('utf-8')), encoding='utf-8',
                  object_pairs_hook=odict)
            except ValueError as ex:
                self.data = None