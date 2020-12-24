# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\srllib\testing\_ifacemock.py
# Compiled at: 2012-05-11 12:09:02
from zope.interface import Interface
from srllib.testing.mock import Mock
import srllib.inspect

class InterfaceMock(Mock):
    """ Mock with special support for zope.interface.
    """

    def __init__(self, *args, **kwds):
        dontMock = kwds['dontMock'] = []
        for name in srllib.inspect.get_members(Interface, callable, include_bases=False):
            dontMock.append(name)

        Mock.__init__(self, *args, **kwds)