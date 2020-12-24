# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/interfaces/bbb.py
# Compiled at: 2008-12-16 18:21:20
from zope.interface import Interface

class ILockable(Interface):
    __module__ = __name__


class INonStealableLock(Interface):
    __module__ = __name__