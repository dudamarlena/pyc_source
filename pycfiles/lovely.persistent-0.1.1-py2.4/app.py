# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/lovely/persistent/app.py
# Compiled at: 2007-12-10 10:14:22
"""
$Id: app.py 82239 2007-12-10 15:14:21Z batlogg $
"""
__docformat__ = 'reStructuredText'
import persistent
_marker = object()

class Persistent(persistent.Persistent):
    __module__ = __name__

    def __setattr__(self, name, value):
        if getattr(self, name, _marker) != value:
            super(Persistent, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name in self.__dict__:
            persistent.Persistent.__delattr__(self, name)