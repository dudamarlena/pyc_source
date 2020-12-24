# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/DpkgDatalist.py
# Compiled at: 2007-11-06 15:08:00
import os, sys
from UserDict import UserDict
from OrderedDict import OrderedDict
import SafeWriteFile
from types import StringType

class DpkgDatalistException(Exception):
    UNKNOWN = 0
    SYNTAXERROR = 1

    def __init__(self, message='', reason=UNKNOWN, file=None, line=None):
        self.message = message
        self.reason = reason
        self.filename = file
        self.line = line


class _DpkgDatalist:

    def __init__(self, fn=''):
        """Initialize a DpkgDatalist object. An optional argument is a
        file from which we load values."""
        self.filename = fn
        if self.filename:
            self.load(self.filename)

    def store(self, fn=None):
        """Store variable data in a file."""
        if fn == None:
            fn = self.filename
        if not fn:
            self._store(sys.stdout)
            return
        if type(fn) == StringType:
            vf = SafeWriteFile(fn + '.new', fn, 'w')
        else:
            vf = fn
        try:
            self._store(vf)
        finally:
            if type(fn) == StringType:
                vf.close()

        return


class DpkgDatalist(UserDict, _DpkgDatalist):

    def __init__(self, fn=''):
        UserDict.__init__(self)
        _DpkgDatalist.__init__(self, fn)


class DpkgOrderedDatalist(OrderedDict, _DpkgDatalist):

    def __init__(self, fn=''):
        OrderedDict.__init__(self)
        _DpkgDatalist.__init__(self, fn)