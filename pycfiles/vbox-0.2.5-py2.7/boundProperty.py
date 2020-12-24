# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\util\boundProperty.py
# Compiled at: 2013-03-15 12:05:06
"""Utility functions."""

def boundProperty(fn):
    origFnName = fn.func_name
    cacheName = ('__cached{}_at_0x{:x}_Value').format(origFnName, id(fn))

    def _bounder(self):
        try:
            return getattr(self, cacheName)
        except AttributeError:
            rv = fn(self)
            if rv is not None:
                setattr(self, cacheName, rv)
            return rv

        return

    return property(_bounder)