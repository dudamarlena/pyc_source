# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/config/configtypes.py
# Compiled at: 2014-01-02 09:31:20


class defaultJSON(object):

    def __init__(self, value):
        self._value = None
        self.setter(value)
        return

    def getter(self):
        return self._value

    def setter(self, value):
        self._value = value

    def toJSON(self):
        return self._value


class nonEmptyStrSetJSON(defaultJSON):

    def setter(self, value):
        self._value = set([ v for v in value if isinstance(v, basestring) and v ])

    def toJSON(self):
        return list(self._value)

    def getter(self):
        return self

    def add(self, v):
        if isinstance(v, basestring) and v:
            self._value.add(v)

    def clear(self):
        self._value.clear()

    def remove(self, v):
        self._value.remove(v)

    def __len__(self):
        return len(self._value)

    def __iter__(self):
        return iter(self._value)

    def __contains__(self, item):
        return self._value.__contains__(item)


class intJSON(defaultJSON):

    def setter(self, value):
        self._value = int(value)


class boolJSON(defaultJSON):

    def setter(self, value):
        self._value = bool(value)


class nonEmptyStrJSON(defaultJSON):

    def setter(self, value):
        if isinstance(value, basestring):
            if len(value) > 0:
                self._value = value
        else:
            raise TypeError('String only')