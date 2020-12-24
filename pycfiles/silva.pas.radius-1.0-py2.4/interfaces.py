# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/silva/pas/radius/interfaces.py
# Compiled at: 2008-11-20 12:49:45
from zope.interface import Interface

class IRaduisAware(Interface):
    """Marker interface to known that the service_members is Raduis
    Aware.
    """
    __module__ = __name__