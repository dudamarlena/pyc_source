# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_http_parser/util.py
# Compiled at: 2020-04-09 00:11:53
# Size of source mod 2**32: 8440 bytes
import sys
from collections import MutableMapping
if sys.version_info[0] == 3:
    from urllib.parse import unquote

    def b(s):
        return s.encode('latin-1')


    def bytes_to_str(b):
        return str(b, 'latin1')


    string_types = (
     str,)
    import io
    StringIO = io.StringIO
    MAXSIZE = sys.maxsize
else:
    from urllib import unquote

    def b(s):
        return s


    def bytes_to_str(s):
        return s


    string_types = (
     basestring,)
    try:
        import cStringIO
        StringIO = BytesIO = cStringIO.StringIO
    except ImportError:
        import StringIO
        StringIO = BytesIO = StringIO.StringIO

    class X(object):

        def __len__(self):
            return 2147483648


    try:
        len(X())
    except OverflowError:
        MAXSIZE = int(2147483647)
    else:
        MAXSIZE = int(9223372036854775807)
    del X

class IOrderedDict(dict, MutableMapping):
    __doc__ = 'Dictionary that remembers insertion order with insensitive key'

    def __init__(self, *args, **kwds):
        """Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.

        """
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self._IOrderedDict__root
        except AttributeError:
            self._IOrderedDict__root = root = [
             None, None, None]
            PREV = 0
            NEXT = 1
            root[PREV] = root[NEXT] = root
            self._IOrderedDict__map = {}

        self._IOrderedDict__lower = {}
        (self.update)(*args, **kwds)

    def __setitem__(self, key, value, PREV=0, NEXT=1, dict_setitem=dict.__setitem__):
        """od.__setitem__(i, y) <==> od[i]=y"""
        if key not in self:
            root = self._IOrderedDict__root
            last = root[PREV]
            last[NEXT] = root[PREV] = self._IOrderedDict__map[key] = [last, root, key]
            self._IOrderedDict__lower[key.lower()] = key
        key = self._IOrderedDict__lower[key.lower()]
        dict_setitem(self, key, value)

    def __delitem__(self, key, PREV=0, NEXT=1, dict_delitem=dict.__delitem__):
        """od.__delitem__(y) <==> del od[y]"""
        if key in self:
            key = self._IOrderedDict__lower.pop(key.lower())
        dict_delitem(self, key)
        link = self._IOrderedDict__map.pop(key)
        link_prev = link[PREV]
        link_next = link[NEXT]
        link_prev[NEXT] = link_next
        link_next[PREV] = link_prev

    def __getitem__(self, key, dict_getitem=dict.__getitem__):
        if key in self:
            key = self._IOrderedDict__lower.get(key.lower())
        return dict_getitem(self, key)

    def __contains__(self, key):
        return key.lower() in self._IOrderedDict__lower

    def __iter__(self, NEXT=1, KEY=2):
        """od.__iter__() <==> iter(od)"""
        root = self._IOrderedDict__root
        curr = root[NEXT]
        while curr is not root:
            yield curr[KEY]
            curr = curr[NEXT]

    def __reversed__(self, PREV=0, KEY=2):
        """od.__reversed__() <==> reversed(od)"""
        root = self._IOrderedDict__root
        curr = root[PREV]
        while curr is not root:
            yield curr[KEY]
            curr = curr[PREV]

    def __reduce__(self):
        """Return state information for pickling"""
        items = [[k, self[k]] for k in self]
        tmp = (self._IOrderedDict__map, self._IOrderedDict__root)
        del self._IOrderedDict__map
        del self._IOrderedDict__root
        inst_dict = vars(self).copy()
        self._IOrderedDict__map, self._IOrderedDict__root = tmp
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        else:
            return (
             self.__class__, (items,))

    def clear(self):
        """od.clear() -> None.  Remove all items from od."""
        try:
            for node in self._IOrderedDict__map.values():
                del node[:]

            self._IOrderedDict__root[:] = [
             self._IOrderedDict__root, self._IOrderedDict__root, None]
            self._IOrderedDict__map.clear()
        except AttributeError:
            pass

        dict.clear(self)

    def get(self, key, default=None):
        if key in self:
            return self[key]
        else:
            return default

    setdefault = MutableMapping.setdefault
    update = MutableMapping.update
    pop = MutableMapping.pop
    keys = MutableMapping.keys
    values = MutableMapping.values
    items = MutableMapping.items
    __ne__ = MutableMapping.__ne__

    def popitem(self, last=True):
        """od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.

        """
        if not self:
            raise KeyError('dictionary is empty')
        key = next(reversed(self) if last else iter(self))
        value = self.pop(key)
        return (key, value)

    def __repr__(self):
        """od.__repr__() <==> repr(od)"""
        if not self:
            return '%s()' % (self.__class__.__name__,)
        else:
            return '%s(%r)' % (self.__class__.__name__, list(self.items()))

    def copy(self):
        """od.copy() -> a shallow copy of od"""
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        """OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
        and values equal to v (which defaults to None).

        """
        d = cls()
        for key in iterable:
            d[key] = value

        return d

    def __eq__(self, other):
        """od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        """
        if isinstance(other, IOrderedDict):
            return len(self) == len(other) and set(self.items()) == set(other.items())
        else:
            return dict.__eq__(self, other)

    def __del__(self):
        self.clear()


status_reasons = {100:'Continue', 
 101:'Switching Protocols', 
 102:'Processing', 
 200:'OK', 
 201:'Created', 
 202:'Accepted', 
 203:'Non Authoritative Information', 
 204:'No Content', 
 205:'Reset Content', 
 206:'Partial Content', 
 207:'Multi Status', 
 226:'IM Used', 
 300:'Multiple Choices', 
 301:'Moved Permanently', 
 302:'Found', 
 303:'See Other', 
 304:'Not Modified', 
 305:'Use Proxy', 
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
 414:'Request URI Too Long', 
 415:'Unsupported Media Type', 
 416:'Requested Range Not Satisfiable', 
 417:'Expectation Failed', 
 422:'Unprocessable Entity', 
 423:'Locked', 
 424:'Failed Dependency', 
 426:'Upgrade Required', 
 500:'Internal Server Error', 
 501:'Not Implemented', 
 502:'Bad Gateway', 
 503:'Service Unavailable', 
 504:'Gateway Timeout', 
 505:'HTTP Version Not Supported', 
 507:'Insufficient Storage', 
 510:'Not Extended'}