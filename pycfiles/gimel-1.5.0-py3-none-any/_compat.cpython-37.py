# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/redis/_compat.py
# Compiled at: 2019-07-06 06:05:05
# Size of source mod 2**32: 2927 bytes
"""Internal module for Python 2 backwards compatibility."""
import sys
if sys.version_info[0] < 3:
    from urllib import unquote
    from urlparse import parse_qs, urlparse
    from itertools import imap, izip
    from string import letters as ascii_letters
    from Queue import Queue
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

    def safe_unicode(obj, *args):
        """ return the unicode representation of obj """
        try:
            return unicode(obj, *args)
        except UnicodeDecodeError:
            ascii_text = str(obj).encode('string_escape')
            return unicode(ascii_text)


    def iteritems(x):
        return x.iteritems()


    def iterkeys(x):
        return x.iterkeys()


    def itervalues(x):
        return x.itervalues()


    def nativestr(x):
        if isinstance(x, str):
            return x
        return x.encode('utf-8', 'replace')


    def u(x):
        return x.decode()


    def b(x):
        return x


    def next(x):
        return x.next()


    def byte_to_chr(x):
        return x


    unichr = unichr
    xrange = xrange
    basestring = basestring
    unicode = unicode
    bytes = str
    long = long
else:
    from urllib.parse import parse_qs, unquote, urlparse
    from io import BytesIO
    from string import ascii_letters
    from queue import Queue

    def iteritems(x):
        return iter(x.items())


    def iterkeys(x):
        return iter(x.keys())


    def itervalues(x):
        return iter(x.values())


    def byte_to_chr(x):
        return chr(x)


    def nativestr(x):
        if isinstance(x, str):
            return x
        return x.decode('utf-8', 'replace')


    def u(x):
        return x


    def b(x):
        if not isinstance(x, bytes):
            return x.encode('latin-1')
        return x


    next = next
    unichr = chr
    imap = map
    izip = zip
    xrange = range
    basestring = str
    unicode = str
    safe_unicode = str
    bytes = bytes
    long = int
try:
    from queue import LifoQueue, Empty, Full
except ImportError:
    from Queue import Empty, Full
    try:
        from Queue import LifoQueue
    except ImportError:
        from Queue import Queue

        class LifoQueue(Queue):
            __doc__ = 'Override queue methods to implement a last-in first-out queue.'

            def _init(self, maxsize):
                self.maxsize = maxsize
                self.queue = []

            def _qsize(self, len=len):
                return len(self.queue)

            def _put(self, item):
                self.queue.append(item)

            def _get(self):
                return self.queue.pop()