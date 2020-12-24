# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/cacheburster/interfaces.py
# Compiled at: 2010-11-18 05:52:41
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.interface.interface import Interface

class IVersionedResourceLayer(IBrowserRequest):
    """A layer that contains all registrations of this package.
    
    It is intended that someone can just use this layer as a base layer when
    using this package."""
    pass


class IVersionManager(Interface):

    def getVersion():
        """Compute version for resource"""
        pass

    def __call__():
        """Get resource version"""
        pass


class IRuleFactory(Interface):

    def __call__(resource):
        """Return an IVersionRule object"""
        pass


class IVersionRule(Interface):

    def check():
        """Is the rule acceptable"""
        pass

    def __call__(request):
        """Process rule"""
        pass