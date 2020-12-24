# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/slc.cart/src/slc/cart/interfaces.py
# Compiled at: 2012-10-31 18:18:01
"""Module where all interfaces, events and exceptions live."""
from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Attribute
from zope.interface import Interface

class ISlcCartLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""
    pass


class ICartAction(Interface):
    """Specification of what a Cart Action needs to provide."""
    name = Attribute('Short id if the action, used in URLs, lookups, etc.')
    title = Attribute('User friendly title of the Cart Action.')
    weight = Attribute('An integer used for sorting the actions.')

    def run():
        """Perform the action."""
        pass


class NoResultError(Exception):
    """Exception if catalog returns zero results."""
    pass