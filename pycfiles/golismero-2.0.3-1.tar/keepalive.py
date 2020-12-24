# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/keepalive/keepalive.py
# Compiled at: 2013-12-09 06:41:17
"""An HTTP handler for urllib2 that supports HTTP 1.1 and keepalive.

  import urllib2
  from keepalive import HTTPHandler
  keepalive_handler = HTTPHandler()
  opener = urllib2.build_opener(keepalive_handler)
  urllib2.install_opener(opener)

  fo = urllib2.urlopen('http://www.python.org')

To remove the handler, simply re-run build_opener with no arguments, and
install that opener.

You can explicitly close connections by using the close_connection()
method of the returned file-like object (described below) or you can
use the handler methods:

  close_connection(host)
  close_all()
  open_connections()

Example:

  keepalive_handler.close_all()

EXTRA ATTRIBUTES AND METHODS

  Upon a status of 200, the object returned has a few additional
  attributes and methods, which should not be used if you want to
  remain consistent with the normal urllib2-returned objects:

    close_connection()  -  close the connection to the host
    readlines()         -  you know, readlines()
    status              -  the return status (ie 404)
    reason              -  english translation of status (ie 'File not found')

  If you want the best of both worlds, use this inside an
  AttributeError-catching try:

    try: status = fo.status
    except AttributeError: status = None

  Unfortunately, these are ONLY there if status == 200, so it's not
  easy to distinguish between non-200 responses.  The reason is that
  urllib2 tries to do clever things with error codes 301, 302, 401,
  and 407, and it wraps the object upon return.

  You can optionally set the module-level global HANDLE_ERRORS to 0,
  in which case the handler will always return the object directly.
  If you like the fancy handling of errors, don't do this.  If you
  prefer to see your error codes, then do.

"""
from httplib import _CS_REQ_STARTED, _CS_REQ_SENT, _CS_IDLE, CannotSendHeader
from lib.core.convert import unicodeencode
from lib.core.data import kb
import threading, urllib2, httplib, socket
VERSION = (0, 1)
DEBUG = 0
HANDLE_ERRORS = 1

class HTTPHandler(urllib2.HTTPHandler):

    def __init__(self):
        self._connections = {}

    def close_connection(self, host):
        """close connection to <host>
        host is the host:port spec, as in 'www.cnn.com:8080' as passed in.
        no error occurs if there is no connection to that host."""
        self._remove_connection(host, close=1)

    def open_connections(self):
        """return a list of connected hosts"""
        retVal = []
        currentThread = threading.currentThread()
        for name, host in self._connections.keys():
            if name == currentThread.getName():
                retVal.append(host)

        return retVal

    def close_all(self):
        """close all open connections"""
        for _, conn in self._connections.items():
            conn.close()

        self._connections = {}

    def _remove_connection(self, host, close=0):
        key = self._get_connection_key(host)
        if self._connections.has_key(key):
            if close:
                self._connections[key].close()
            del self._connections[key]

    def _get_connection_key(self, host):
        return (threading.currentThread().getName(), host)

    def _start_connection(self, h, req):
        h.clearheaders()
        try:
            if req.has_data():
                data = req.get_data()
                h.putrequest('POST', req.get_selector())
                if not req.headers.has_key('Content-type'):
                    req.headers['Content-type'] = 'application/x-www-form-urlencoded'
                if not req.headers.has_key('Content-length'):
                    req.headers['Content-length'] = '%d' % len(data)
            else:
                h.putrequest(req.get_method() or 'GET', req.get_selector())
            if not req.headers.has_key('Connection'):
                req.headers['Connection'] = 'keep-alive'
            for args in self.parent.addheaders:
                h.putheader(*args)

            for k, v in req.headers.items():
                h.putheader(k, v)

            h.endheaders()
            if req.has_data():
                h.send(data)
        except socket.error as err:
            h.close()
            raise urllib2.URLError(err)

    def do_open(self, http_class, req):
        global HANDLE_ERRORS
        h = None
        host = req.get_host()
        if not host:
            raise urllib2.URLError('no host given')
        try:
            need_new_connection = 1
            key = self._get_connection_key(host)
            h = self._connections.get(key)
            if h is not None:
                try:
                    self._start_connection(h, req)
                except:
                    r = None
                else:
                    try:
                        r = h.getresponse()
                    except httplib.ResponseNotReady as e:
                        r = None
                    except httplib.BadStatusLine as e:
                        r = None

                if r is None or r.version == 9:
                    if DEBUG:
                        print 'failed to re-use connection to %s' % host
                    h.close()
                else:
                    if DEBUG:
                        print 're-using connection to %s' % host
                    need_new_connection = 0
            if need_new_connection:
                if DEBUG:
                    print 'creating new connection to %s' % host
                h = http_class(host)
                self._connections[key] = h
                self._start_connection(h, req)
                r = h.getresponse()
        except socket.error as err:
            if h:
                h.close()
            raise urllib2.URLError(err)

        if r.will_close:
            self._remove_connection(host)
        if DEBUG:
            print 'STATUS: %s, %s' % (r.status, r.reason)
        r._handler = self
        r._host = host
        r._url = req.get_full_url()
        if r.status == 200 or not HANDLE_ERRORS:
            resp = urllib2.addinfourl(r, r.msg, req.get_full_url())
            resp.code = r.status
            resp.msg = r.reason
            return resp
        else:
            r.code = r.status
            return self.parent.error('http', req, r, r.status, r.reason, r.msg)
            return

    def http_open(self, req):
        return self.do_open(HTTPConnection, req)


class HTTPResponse(httplib.HTTPResponse):

    def __init__(self, sock, debuglevel=0, strict=0, method=None):
        if method:
            httplib.HTTPResponse.__init__(self, sock, debuglevel, method)
        else:
            httplib.HTTPResponse.__init__(self, sock, debuglevel)
        self.fileno = sock.fileno
        self._method = method
        self._rbuf = ''
        self._rbufsize = 8096
        self._handler = None
        self._host = None
        self._url = None
        return

    _raw_read = httplib.HTTPResponse.read

    def close_connection(self):
        self.close()
        self._handler._remove_connection(self._host, close=1)

    def info(self):
        return self.msg

    def geturl(self):
        return self._url

    def read(self, amt=None):
        if self._rbuf and amt is not None:
            L = len(self._rbuf)
            if amt > L:
                amt -= L
            else:
                s = self._rbuf[:amt]
                self._rbuf = self._rbuf[amt:]
                return s
        s = self._rbuf + self._raw_read(amt)
        self._rbuf = ''
        return s

    def readline(self, limit=-1):
        data = ''
        i = self._rbuf.find('\n')
        while i < 0 and not 0 < limit <= len(self._rbuf):
            new = self._raw_read(self._rbufsize)
            if not new:
                break
            i = new.find('\n')
            if i >= 0:
                i = i + len(self._rbuf)
            self._rbuf = self._rbuf + new

        if i < 0:
            i = len(self._rbuf)
        else:
            i = i + 1
        if 0 <= limit < len(self._rbuf):
            i = limit
        data, self._rbuf = self._rbuf[:i], self._rbuf[i:]
        return data

    def readlines(self, sizehint=0):
        total = 0
        list = []
        while 1:
            line = self.readline()
            if not line:
                break
            list.append(line)
            total += len(line)
            if sizehint and total >= sizehint:
                break

        return list


class HTTPConnection(httplib.HTTPConnection):
    response_class = HTTPResponse
    _headers = None

    def clearheaders(self):
        self._headers = {}

    def putheader(self, header, value):
        """Send a request header line to the server.

        For example: h.putheader('Accept', 'text/html')
        """
        if self.__state != _CS_REQ_STARTED:
            raise CannotSendHeader()
        self._headers[header] = value

    def endheaders(self):
        """Indicate that the last header line has been sent to the server."""
        if self.__state == _CS_REQ_STARTED:
            self.__state = _CS_REQ_SENT
        else:
            raise CannotSendHeader()
        for header in ('Host', 'Accept-Encoding'):
            if header in self._headers:
                str = '%s: %s' % (header, self._headers[header])
                self._output(str)
                del self._headers[header]

        for header, value in self._headers.items():
            str = '%s: %s' % (header, value)
            self._output(str)

        self._send_output()

    def send(self, str):
        httplib.HTTPConnection.send(self, unicodeencode(str, kb.pageEncoding))


def error_handler(url):
    global HANDLE_ERRORS
    orig = HANDLE_ERRORS
    keepalive_handler = HTTPHandler()
    opener = urllib2.build_opener(keepalive_handler)
    urllib2.install_opener(opener)
    pos = {0: 'off', 1: 'on'}
    for i in (0, 1):
        print '  fancy error handling %s (HANDLE_ERRORS = %i)' % (pos[i], i)
        HANDLE_ERRORS = i
        try:
            fo = urllib2.urlopen(url)
            foo = fo.read()
            fo.close()
            try:
                status, reason = fo.status, fo.reason
            except AttributeError:
                status, reason = (None, None)

        except IOError as e:
            print '  EXCEPTION: %s' % e
            raise
        else:
            print '  status = %s, reason = %s' % (status, reason)

    HANDLE_ERRORS = orig
    hosts = keepalive_handler.open_connections()
    print 'open connections:', (' ').join(hosts)
    keepalive_handler.close_all()
    return


def continuity(url):
    import md5
    format = '%25s: %s'
    opener = urllib2.build_opener()
    urllib2.install_opener(opener)
    fo = urllib2.urlopen(url)
    foo = fo.read()
    fo.close()
    m = md5.new(foo)
    print format % ('normal urllib', m.hexdigest())
    opener = urllib2.build_opener(HTTPHandler())
    urllib2.install_opener(opener)
    fo = urllib2.urlopen(url)
    foo = fo.read()
    fo.close()
    m = md5.new(foo)
    print format % ('keepalive read', m.hexdigest())
    fo = urllib2.urlopen(url)
    foo = ''
    while 1:
        f = fo.readline()
        if f:
            foo = foo + f
        else:
            break

    fo.close()
    m = md5.new(foo)
    print format % ('keepalive readline', m.hexdigest())


def comp(N, url):
    print '  making %i connections to:\n  %s' % (N, url)
    sys.stdout.write('  first using the normal urllib handlers')
    opener = urllib2.build_opener()
    urllib2.install_opener(opener)
    t1 = fetch(N, url)
    print '  TIME: %.3f s' % t1
    sys.stdout.write('  now using the keepalive handler       ')
    opener = urllib2.build_opener(HTTPHandler())
    urllib2.install_opener(opener)
    t2 = fetch(N, url)
    print '  TIME: %.3f s' % t2
    print '  improvement factor: %.2f' % (t1 / t2,)


def fetch(N, url, delay=0):
    lens = []
    starttime = time.time()
    for i in xrange(N):
        if delay and i > 0:
            time.sleep(delay)
        fo = urllib2.urlopen(url)
        foo = fo.read()
        fo.close()
        lens.append(len(foo))

    diff = time.time() - starttime
    j = 0
    for i in lens[1:]:
        j = j + 1
        if not i == lens[0]:
            print 'WARNING: inconsistent length on read %i: %i' % (j, i)

    return diff


def test(url, N=10):
    print 'checking error hander (do this on a non-200)'
    try:
        error_handler(url)
    except IOError as e:
        print 'exiting - exception will prevent further tests'
        sys.exit()

    print
    print "performing continuity test (making sure stuff isn't corrupted)"
    continuity(url)
    print
    print 'performing speed comparison'
    comp(N, url)


if __name__ == '__main__':
    import time, sys
    try:
        N = int(sys.argv[1])
        url = sys.argv[2]
    except:
        print '%s <integer> <url>' % sys.argv[0]
    else:
        test(url, N)