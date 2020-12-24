# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\piano\resources\interfaces.py
# Compiled at: 2012-03-22 14:35:21
"""
:mod:`piano.resources.interfaces`
---------------------------------

.. autoclass:: IApp

.. autoclass:: ISite
   
"""
from zope.interface import Interface

class IApp(Interface):
    """Marker interface for an application context.
    """
    pass


class ISite(Interface):
    """Marker interface for a site context.
    """
    pass