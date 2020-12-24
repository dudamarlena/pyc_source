# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ctxtnavadd/api.py
# Compiled at: 2006-06-04 21:14:20
from trac.core import *

class ICtxtnavAdder(Interface):
    """An extension point interface to adding ctxtnav entries."""
    __module__ = __name__

    def match_ctxtnav_add(req):
        """Return True if you want to alter this requests ctxtnav bar."""
        pass

    def get_ctxtnav_adds(req):
        """Return a list of the form (path, text) to be added to the bar."""
        pass