# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend/utils.py
# Compiled at: 2008-06-09 19:08:17
"""

utils.py
========

Misc utilities for doapfiend
----------------------------

General purpose helper functions and classes for doapfiend
You'll probably want to use doaplib for most cases.

License: BSD-2

"""
import urllib, logging, urlparse
from httplib import HTTPConnection
from urllib2 import build_opener, HTTPError, ProxyHandler, URLError
__docformat__ = 'epytext'
LOG = logging.getLogger('doapfiend')
COLOR = {'normal': '\x1b[0m', 'bold': '\x1b[1m', 
   'underline': '\x1b[4m', 
   'blink': '\x1b[5m', 
   'reverse': '\x1b[7m', 
   'black': '\x1b[30m', 
   'red': '\x1b[31m', 
   'green': '\x1b[32m', 
   'yellow': '\x1b[33m', 
   'blue': '\x1b[34m', 
   'magenta': '\x1b[35m', 
   'cyan': '\x1b[36m', 
   'white': '\x1b[37m'}

class NotFoundError(Exception):
    """DOAP not found"""

    def __init__(self, err_msg):
        """Initialize attributes"""
        self.err_msg = err_msg

    def __str__(self):
        return repr(self.err_msg)


def http_filesize(url):
    """
    Get the size of file without downloading it.
    bla bla bla
    blaba

    @param url: URL of file
    @type  url: string

    @rtype: string
    @return: Size of file

    Usage:

    >>> http_filesize('http://trac.doapspace.org/test_file.txt')
    '160'
    """
    (host, path) = urlparse.urlsplit(url)[1:3]
    if ':' in host:
        (host, port) = host.split(':', 1)
        try:
            port = int(port)
        except ValueError:
            LOG.error('invalid port number %r' % port)
            return False

    else:
        port = None
    connection = HTTPConnection(host, port=port)
    connection.request('HEAD', path)
    resp = connection.getresponse()
    return resp.getheader('content-length')


def http_exists(url):
    """
    A quick way to check if a file exists on the web.

    @param url: URL of the document
    @type  url: string
    @rtype: boolean
    @return:  True or False

    Usage:

    >>> http_exists('http://www.python.org/')
    True
    >>> http_exists('http://www.python.org/PenguinOnTheTelly')
    False
    """
    (host, path) = urlparse.urlsplit(url)[1:3]
    if ':' in host:
        (host, port) = host.split(':', 1)
        try:
            port = int(port)
        except ValueError:
            LOG.error('invalid port number %r' % port)
            return False

    else:
        port = None
    connection = HTTPConnection(host, port=port)
    connection.request('HEAD', path)
    resp = connection.getresponse()
    if resp.status == 200:
        found = True
    elif resp.status == 302:
        found = http_exists(urlparse.urljoin(url, resp.getheader('location', '')))
    else:
        LOG.info('Status %d %s : %s' % (resp.status, resp.reason, url))
        found = False
    return found


def is_content_type(url_or_file, content_type):
    """
    Tells whether the URL or pseudofile from urllib.urlopen is of
    the required content type.

    @param url_or_file: URL or file path
    @type url_or_file: string
    @param content_type: Content type we're looking for
    @type content_type: string

    @rtype: boolean
    @returns: True if it can return the Content type we want

    Usage:

    >>> is_content_type('http://doapspace.org/doap/sf/nlyrics.rdf',             'application/rdf+xml')
    True
    >>> is_content_type('http://doapspace.org/', 'application/rdf+xml')
    False
    """
    try:
        if isinstance(url_or_file, str):
            thefile = urllib.urlopen(url_or_file)
        else:
            thefile = url_or_file
        result = thefile.info().gettype() == content_type.lower()
        if thefile is not url_or_file:
            thefile.close()
    except IOError:
        result = False

    return result


def fetch_file(url, proxy=None):
    """
    Download file by URL

    @param url: URL of a file
    @type url: string

    @param proxy: URL of HTTP Proxy
    @type proxy: string

    @return: File
    @rtype: string

    """
    if not url.startswith('http://') and not url.startswith('ftp://'):
        try:
            return open(url, 'r').read()
        except IOError, errmsg:
            LOG.error(errmsg)
            return ''

    LOG.debug('Fetching ' + url)
    if proxy:
        opener = build_opener(ProxyHandler({'http': proxy}))
    else:
        opener = build_opener()
    opener.addheaders = [
     ('Accept', 'application/rdf+xml'),
     (
      'User-agent',
      'Mozilla/5.0 (compatible; doapfiend ' + 'http://trac.doapspace.org/doapfiend)')]
    try:
        result = opener.open(url)
    except HTTPError, err_msg:
        if err_msg.code == 404:
            raise NotFoundError('Not found: %s' % url)
        else:
            LOG.error(err_msg)
    except URLError, err_msg:
        LOG.error(err_msg)
        return

    return result.read()


if __name__ == '__main__':
    import doctest
    doctest.testmod()