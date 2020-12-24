# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/utils.py
# Compiled at: 2011-04-29 08:23:12
import sys, pkg_resources, urllib, urllib2, urlparse, httplib, socket, logging, HTMLParser
try:
    set
except NameError:
    from sets import Set as set

version = pkg_resources.get_distribution('LinkExchange').version
default_user_agent = 'LinkExchange/%s (+http://linkexchange.org.ua)' % version

def is_plugin_specifier(x):
    return type(x) in (list, tuple)


def load_plugin(space, specifier):
    specifier = list(specifier)
    name = specifier.pop(0)
    if specifier:
        args = specifier.pop(0)
    else:
        args = []
    if specifier:
        kwargs = specifier.pop(0)
    else:
        kwargs = {}
    error = None
    for ep in pkg_resources.iter_entry_points(space, name):
        try:
            cls = ep.load()
        except ImportError as e:
            error = e
        else:
            return cls(*args, **kwargs)

    if error:
        raise e
    raise ImportError('No entry point found: %s.%s' % (space, name))
    return


def urlopen_with_timeout(url, timeout):
    """
    Opens URL with timeout. Returns file-like object.

    >>> import threading
    >>> import BaseHTTPServer, SimpleHTTPServer
    >>> addr, port = ('127.0.0.1', 49152)
    >>> url = 'http://%s:%d' % (addr, port)
    >>> ready = threading.Event()
    >>> shutdown = threading.Event()
    >>> def serve():
    ...     srv = BaseHTTPServer.HTTPServer((addr, port),
    ...             SimpleHTTPServer.SimpleHTTPRequestHandler)
    ...     ready.set()
    ...     srv.handle_request()
    ...     shutdown.wait()

    >>> srv_t = threading.Thread(target=serve)
    >>> srv_t.start()
    >>> ignore = ready.wait()
    >>> f = urlopen_with_timeout(url, 0.1)
    >>> 'content-type' in f.info()
    True
    >>> try: f = urlopen_with_timeout(url, 0.1)
    ... except urlopen_errors: f = None
    >>> f is None
    True
    >>> shutdown.set()
    >>> srv_t.join()
    """
    if sys.version_info >= (2, 6):
        return urllib2.urlopen(url, None, timeout)
    else:

        class _NonBlockingHTTPConnection(httplib.HTTPConnection):

            def connect(self):
                httplib.HTTPConnection.connect(self)
                self.sock.settimeout(timeout)

        if sys.version_info < (2, 4):

            class _NonBlockingHTTP(httplib.HTTP):
                _connection_class = _NonBlockingHTTPConnection

        class _NonBlockingHTTPHandler(urllib2.HTTPHandler):

            def http_open(self, req):
                if sys.version_info < (2, 4):
                    return self.do_open(_NonBlockingHTTP, req)
                return self.do_open(_NonBlockingHTTPConnection, req)

        return urllib2.build_opener(_NonBlockingHTTPHandler).open(url)


urlopen_errors = (urllib2.URLError, httplib.HTTPException, OSError,
 socket.error, socket.herror, socket.gaierror, socket.timeout)

def normalize_uri(uri):
    if isinstance(uri, unicode):
        uri = uri.encode('utf-8')
    s, n, p, q, f = urlparse.urlsplit(uri)
    p = urllib.quote(urllib.unquote(p), '/')
    p = p[:1] + p[1:].rstrip('/')
    return urlparse.urlunsplit((s, n, p, q, f))


def rearrange_blocks(request, blocks, rearrange_map=None):
    """
    Rearranges links blocks according to rearrange_map and depending of request
    URI.

    >>> from linkexchange.clients import PageRequest
    >>> request = PageRequest(host='example.com', uri='/')
    >>> ord('/')
    47
    >>> blocks = [u'b1', u'b2', u'b3']
    >>> rearrange_map = [(0, 2, 0, 3), (2, 3, 3, 5)]
    >>> rearrange_blocks(request, blocks, rearrange_map)
    [u'b2', u'', u'b1', u'', u'b3']
    """
    if rearrange_map is None:
        rearrange_map = [
         (
          0, len(blocks), 0, len(blocks))]
    req_sum = sum([ ord(x) for x in request.uri ])
    result_dic = {}
    result_len = 0
    for i1, i2, o1, o2 in rearrange_map:
        ia = blocks[i1:i2]
        oi = o1 + req_sum % (o2 - o1)
        while ia:
            if oi not in result_dic:
                result_dic[oi] = ia.pop(0)
            oi += 1
            if oi >= o2:
                oi = o1

        if o2 > result_len:
            result_len = o2

    return [ result_dic.get(i, '') for i in range(0, result_len) ]


def parse_rearrange_map(map_str):
    """
    Parse rearrange map string as it specified in the configuration file.

    >>> parse_rearrange_map('0:1-0:3,1:2-3:5,2:3-0:3')
    [(0, 1, 0, 3), (1, 2, 3, 5), (2, 3, 0, 3)]
    """

    def parse_entry(entry):
        entry = entry.strip()
        i, o = entry.split('-')
        i1, i2 = i.split(':')
        o1, o2 = o.split(':')
        return (int(i1), int(i2), int(o1), int(o2))

    try:
        return map(parse_entry, map_str.split(','))
    except ValueError:
        raise ValueError('Invalid rearrange map string')


def configure_logger(handler=None, formatter=None, level=None):
    logger = logging.getLogger('linkexchange')
    if handler is None:
        handler = logging.StreamHandler()
        if formatter is None:
            formatter = logging.Formatter('%(levelname)s: %(message)s')
        handler.setFormatter(formatter)
    try:
        logger.removeHandler(logger._lx_handler)
    except AttributeError:
        pass

    logger.addHandler(handler)
    logger._lx_handler = handler
    if level is not None:
        logger.setLevel(level)
    return


class LinkFinder(HTMLParser.HTMLParser):

    def __init__(self, found_callback=None):
        HTMLParser.HTMLParser.__init__(self)
        self.char_buf = []
        self.links = []
        if found_callback is None:
            found_callback = lambda *args: self.links.append(args)
        self.found_callback = found_callback
        self.exclude_tags = set(['a',
         'textarea', 'select', 'script', 'style',
         'label', 'noscript', 'noindex', 'button'])
        self.exclude_ctx = []
        self.in_link = False
        return

    def handle_starttag(self, tag, attrs):
        self.handle_realdata()
        if tag == 'a' and not self.exclude_ctx:
            self.in_link = True
            self.in_link_attrs = attrs
            self.in_link_text = ''
        if tag in self.exclude_tags:
            self.exclude_ctx.append(tag)

    def handle_endtag(self, tag):
        self.handle_realdata()
        if tag == 'a' and self.in_link:
            self.found_callback(dict(self.in_link_attrs), self.in_link_text)
            self.in_link = False
        if tag in self.exclude_tags:
            self.exclude_ctx.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_realdata()

    def handle_data(self, data):
        self.char_buf.append(data)

    def handle_charref(self, name):
        self.char_buf.append('&#%s;' % name)

    def handle_entityref(self, name):
        self.char_buf.append('&%s;' % name)

    def handle_realdata(self):
        content = ('').join(self.char_buf)
        self.char_buf[:] = []
        if self.in_link:
            self.in_link_text += content


def find_links(html):
    """
    Searches for links in HTML code.

    >>> find_links('<p>Some text <a href="/ref">with link</a>.</p>')
    [({'href': '/ref'}, 'with link')]
    """
    finder = LinkFinder()
    finder.feed(html)
    finder.close()
    return finder.links


if __name__ == '__main__':
    import doctest
    doctest.testmod()