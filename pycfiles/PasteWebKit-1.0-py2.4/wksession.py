# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/wksession.py
# Compiled at: 2006-10-22 17:01:02
"""
The WebKit session object; an interface surrounding a persistent
dictionary.
"""
from wkcommon import NoDefault

class Session:
    __module__ = __name__

    def __init__(self, dict):
        self._values = dict

    def invalidate(self):
        self._values.clear()

    def value(self, name, default=NoDefault):
        if default is NoDefault:
            return self._values[name]
        else:
            return self._values.get(name, default)

    def hasValue(self, name):
        return self._values.has_key(name)

    def setValue(self, name, value):
        self._values[name] = value

    def delValue(self, name):
        del self._values[name]

    def values(self):
        return self._values

    def setTimeout(self, timeout):
        pass

    def __getitem__(self, name):
        return self.value(name)

    def __setitem__(self, name, value):
        self.setValue(name, value)

    def __delitem__(self, name):
        self.delValue(name)