# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/headersdict.py
# Compiled at: 2013-08-10 12:52:27
from header import Header

class HeadersDict(object):

    def __init__(self, initial_data=None):
        self._headers = []
        if initial_data:
            self.update(initial_data)

    def __setitem__(self, key, value):
        self._set_header(key, value)

    def __getitem__(self, key):
        header = self._get_header(key)
        if not header:
            raise KeyError(key)
        return header

    def __delitem__(self, key):
        self._headers.remove(self[key])

    def __contains__(self, key):
        return bool(self._get_header(key))

    def __len__(self):
        return len(self._headers)

    def __repr__(self):
        temp = {}
        for i in self._headers:
            temp[i.key] = i.value

        return repr(temp)

    def __str__(self):
        return self.render()

    def _set_header(self, key, value):
        header = self._get_header(key)
        if not header:
            header = Header(key, value)
            self._headers.append(header)
        else:
            header.value = value
        return self

    def _get_header(self, key):
        for header in self._headers:
            if header.key == key:
                return header

        return

    def keys(self):
        keys = [ i.key for i in self._headers ]
        return list(set(keys))

    def values(self):
        return [ i.value for i in self._headers ]

    def items(self):
        return [ (i.key, i.value) for i in self._headers ]

    def iteritems(self):
        for i in self._headers:
            yield (
             i.key, i.value)

    def update(self, data):
        for key, value in data.iteritems():
            self[key] = value

    def add_header(self, header):
        self._headers.append(header)

    def del_header(self, header):
        self._headers.remove(header)

    def render(self):
        return ('\r\n').join(map(str, self._headers)) + '\r\n\r\n'

    def copy(self):
        copy = HeaderList()
        copy._headers = list(self._headers)

    def clear(self):
        del self._headers[:]

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default