# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-whg15vss\serial\serial\request.py
# Compiled at: 2019-09-23 04:34:10
# Size of source mod 2**32: 14226 bytes
"""
This module extends the functionality of `urllib.request.Request` to support multipart requests, to support passing
instances of serial models to the `data` parameter/property for `urllib.request.Request`, and to
support casting requests as `str` or `bytes` (typically for debugging purposes and/or to aid in producing
non-language-specific API documentation).
"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from utilities.compatibility import backport
backport()
from future.utils import native_str
import random, re, string, urllib.request
try:
    from typing import Dict, Sequence, Set, Iterable
except ImportError:
    Dict = Sequence = Set = None

from serial.marshal import serialize
from abc.model import Model
from .utilities import collections_abc

class Headers(object):
    __doc__ = '\n    A dictionary of headers for a `Request`, `Part`, or `MultipartRequest` instance.\n    '

    def __init__(self, items, request):
        self._dict = {}
        self.request = request
        self.update(items)

    def pop(self, key, default=None):
        key = key.capitalize()
        if hasattr(self.request, '_boundary'):
            self.request._boundary = None
        if hasattr(self.request, '_bytes'):
            self.request._bytes = None
        return self._dict.pop(key, default=default)

    def popitem(self):
        if hasattr(self.request, '_boundary'):
            self.request._boundary = None
        if hasattr(self.request, '_bytes'):
            self.request._bytes = None
        return self._dict.popitem()

    def setdefault(self, key, default=None):
        key = key.capitalize()
        if hasattr(self.request, '_boundary'):
            self.request._boundary = None
        if hasattr(self.request, '_bytes'):
            self.request._bytes = None
        return self._dict.setdefault(key, default=default)

    def update(self, iterable=None, **kwargs):
        cd = {}
        if iterable is None:
            d = kwargs
        else:
            d = dict(iterable, **kwargs)
        for k, v in d.items():
            cd[k.capitalize()] = v

        if hasattr(self.request, '_boundary'):
            self.request._boundary = None
        if hasattr(self.request, '_bytes'):
            self.request._bytes = None
        return self._dict.update(cd)

    def __delitem__(self, key):
        key = key.capitalize()
        if hasattr(self.request, '_boundary'):
            self.request._boundary = None
        if hasattr(self.request, '_bytes'):
            self.request._bytes = None
        del self._dict[key]

    def __setitem__(self, key, value):
        key = key.capitalize()
        if key != 'Content-length':
            if hasattr(self.request, '_boundary'):
                self.request._boundary = None
            if hasattr(self.request, '_bytes'):
                self.request._bytes = None
            return self._dict.__setitem__(key, value)

    def __getitem__(self, key):
        key = key.capitalize()
        if key == 'Content-length':
            data = self.request.data
            if data is None:
                content_length = 0
            else:
                content_length = len(data)
            value = str(content_length)
        else:
            try:
                value = self._dict.__getitem__(key)
            except KeyError as e:
                try:
                    if key == 'Content-type':
                        if hasattr(self.request, 'parts'):
                            if self.request.parts:
                                value = 'multipart/form-data'
                finally:
                    e = None
                    del e

            if value is not None:
                if value.strip().lower()[:9] == 'multipart':
                    if hasattr(self.request, 'boundary'):
                        value += '; boundary=' + str((self.request.boundary), encoding='utf-8')
        return value

    def keys(self):
        return (k for k in self)

    def values(self):
        return (self[k] for k in self)

    def __len__(self):
        return len(tuple(self))

    def __iter__(self):
        keys = set()
        for k in self._dict.keys():
            keys.add(k)
            yield k

        if type(self.request) is not Part:
            if 'Content-length' not in keys:
                yield 'Content-length'
        if hasattr(self.request, 'parts'):
            if self.request.parts:
                if 'Content-type' not in keys:
                    yield 'Content-type'

    def __contains__(self, key):
        if key in self.keys():
            return True
        return False

    def items(self):
        for k in self:
            yield (
             k, self[k])

    def copy(self):
        return self.__class__((self._dict),
          request=(self.request))

    def __copy__(self):
        return self.copy()


class Data(object):
    __doc__ = "\n    One of a multipart request's parts.\n    "

    def __init__(self, data=None, headers=None):
        """
        Parameters:

            - data (bytes|str|collections.Sequence|collections.Set|dict|serial.abc.Model): The payload.

            - headers ({str: str}): A dictionary of headers (for this part of the request body, not the main request).
              This should (almost) always include values for "Content-Disposition" and "Content-Type".
        """
        self._bytes = None
        self._headers = None
        self._data = None
        self.headers = headers
        self.data = data

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._bytes = None
        if headers is None:
            headers = Headers({}, self)
        else:
            if isinstance(headers, Headers):
                headers.request = self
            else:
                headers = Headers(headers, self)
        self._headers = headers

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._bytes = None
        if data is not None:
            serialize_type = None
            if 'Content-type' in self.headers:
                ct = self.headers['Content-type']
                if re.search('/json\\b', ct) is not None:
                    serialize_type = 'json'
                if re.search('/xml\\b', ct) is not None:
                    serialize_type = 'xml'
                if re.search('/yaml\\b', ct) is not None:
                    serialize_type = 'yaml'
            else:
                if (isinstance(data, (Model, dict)) or isinstance)(data, (collections_abc.Sequence, collections_abc.Set)) and not isinstance(data, (str, bytes)):
                    data = serialize(data, serialize_type or 'json')
            if isinstance(data, str):
                data = bytes(data, encoding='utf-8')
        self._data = data

    def __bytes__(self):
        if self._bytes is None:
            lines = []
            for k, v in self.headers.items():
                lines.append(bytes(('%s: %s' % (k, v)),
                  encoding='utf-8'))

            lines.append(b'')
            data = self.data
            if data:
                lines.append(self.data)
            self._bytes = (b'\r\n').join(lines) + b'\r\n'
        return self._bytes

    def __str__(self):
        b = self.__bytes__()
        if not isinstance(b, native_str):
            b = repr(b)[2:-1].replace('\\r\\n', '\r\n').replace('\\n', '\n')
        return b


class Part(Data):

    def __init__(self, data=None, headers=None, parts=None):
        """
        Parameters:

            - data (bytes|str|collections.Sequence|collections.Set|dict|serial.abc.Model): The payload.

            - headers ({str: str}): A dictionary of headers (for this part of the request body, not the main request).
              This should (almost) always include values for "Content-Disposition" and "Content-Type".
        """
        self._boundary = None
        self._parts = None
        self.parts = parts
        Data.__init__(self, data=data, headers=headers)

    @property
    def boundary(self):
        """
        Calculates a boundary which is not contained in any of the request parts.
        """
        if self._boundary is None:
            data = (b'\r\n').join([
             self._data or b''] + [bytes(p) for p in self.parts])
            boundary = (b'').join((bytes((random.choice(string.digits + string.ascii_letters)), encoding='utf-8') for i in range(16)))
            while boundary in data:
                boundary += bytes((random.choice(string.digits + string.ascii_letters)),
                  encoding='utf-8')

            self._boundary = boundary
        return self._boundary

    @property
    def data(self):
        if self.parts:
            data = (b'\r\n--' + self.boundary + b'\r\n').join([
             self._data or b''] + [bytes(p).rstrip() for p in self.parts]) + (b'\r\n--' + self.boundary + b'--')
        else:
            data = self._data
        return data

    @data.setter
    def data(self, data):
        return Data.data.__set__(self, data)

    @property
    def parts(self):
        return self._parts

    @parts.setter
    def parts(self, parts):
        if parts is None:
            parts = Parts([], request=self)
        else:
            if isinstance(parts, Parts):
                parts.request = self
            else:
                parts = Parts(parts, request=self)
        self._boundary = None
        self._parts = parts


class Parts(list):

    def __init__(self, items, request):
        self.request = request
        super().__init__(items)

    def append(self, item):
        self.request._boundary = None
        self.request._bytes = None
        super().append(item)

    def clear(self):
        self.request._boundary = None
        self.request._bytes = None
        super().clear()

    def extend(self, items):
        self.request._boundary = None
        self.request._bytes = None
        super().extend(items)

    def reverse(self):
        self.request._boundary = None
        self.request._bytes = None
        super().reverse()

    def __delitem__(self, key):
        self.request._boundary = None
        self.request._bytes = None
        super().__delitem__(key)

    def __setitem__(self, key, value):
        self.request._boundary = None
        self.request._bytes = None
        super().__setitem__(key, value)


class Request(Data, urllib.request.Request):
    __doc__ = '\n    A sub-class of `urllib.request.Request` which accommodates additional data types, and serializes `data` in\n    accordance with what is indicated by the request\'s "Content-Type" header.\n    '

    def __init__(self, url, data=None, headers=None, origin_req_host=None, unverifiable=False, method=None):
        self._bytes = None
        self._headers = None
        self._data = None
        self.headers = headers
        urllib.request.Request.__init__(self,
          url,
          data=data,
          headers=headers,
          origin_req_host=origin_req_host,
          unverifiable=unverifiable,
          method=method)


class MultipartRequest(Part, Request):
    __doc__ = '\n    A sub-class of `Request` which adds a property (and initialization parameter) to hold the `parts` of a\n    multipart request.\n\n    https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html\n    '

    def __init__(self, url, data=None, headers=None, origin_req_host=None, unverifiable=False, method=None, parts=None):
        Part.__init__(self,
          data=data,
          headers=headers,
          parts=parts)
        Request.__init__(self,
          url,
          data=data,
          headers=headers,
          origin_req_host=origin_req_host,
          unverifiable=unverifiable,
          method=method)