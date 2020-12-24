# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimageadapter/smartimagecontainer.py
# Compiled at: 2008-12-23 17:55:56
"""SmartImageContainerAdapter for the Zope 3 based smartimage package

$Id: smartimagecontainer.py 12459 2007-10-25 19:39:55Z anton $
"""
__author__ = 'Andrey Orlov'
__license__ = 'ZPL'
__version__ = '$Revision: 12459 $'
__date__ = '$Date: 2007-10-25 22:39:55 +0300 (Thu, 25 Oct 2007) $'
from zope.interface import implements
from zope.publisher.browser import BrowserView
from interfaces import ISmartImageContainer, ISmartImageCached
from zope.location.interfaces import ILocation
from zope.component import ComponentLookupError, getUtility
from ks.smartimage.smartimagecache.interfaces import ISmartImageProp
from smartimagecached import SmartImageCached
from logging import getLogger
logger = getLogger('ks.smartimage')

class SmartImageContainerAdapter(object):
    """Контейнер отмасштабированных изображений """
    __module__ = __name__
    implements(ISmartImageContainer)
    __name__ = '@@smartimagecontainer'
    scales = []
    ignore = False

    def __init__(self, context):
        self.context = context
        self.scales = [ scale.name for scale in getUtility(ISmartImageProp).scales ]

    def __contains__(self, key):
        return key in self.scales or self.ignore

    def items(self):
        return [ (key, self[key]) for key in self.keys() ]

    def keys(self):
        return self.scales[:]

    def values(self):
        return [ self[key] for key in self.keys() ]

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, name):
        return SmartImageCached(self, name)

    def get(self, name, d):
        try:
            return self[name]
        except KeyError:
            return d


class SmartImageContainerView(SmartImageContainerAdapter, BrowserView):
    """Контейнер отмасштабированных изображений """
    __module__ = __name__
    implements(ILocation)

    def __init__(self, context, request):
        self.__parent__ = context
        BrowserView.__init__(self, context, request)
        SmartImageContainerAdapter.__init__(self, context)