# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimageadapter/smartimagebyid.py
# Compiled at: 2008-12-23 17:55:56
"""SmartImageSelectAdapter for the Zope 3 based smartimage package

$Id: smartimagebyid.py 12280 2007-10-12 10:35:47Z cray $
"""
__author__ = 'Andrey Orlov'
__license__ = 'ZPL'
__version__ = '$Revision: 12280 $'
__date__ = '$Date: 2007-10-12 13:35:47 +0300 (Fri, 12 Oct 2007) $'
from zope.interface import implements
from zope.publisher.browser import BrowserView
from interfaces import ISmartImageById, ISmartImageContainer, ISmartImageCached
from zope.location.interfaces import ILocation
from zope.component import getUtility
from ks.smartimage.smartimagecache.interfaces import ISmartImageProp
from smartimagecontainer import SmartImageContainerView
from logging import getLogger
logger = getLogger('ks.smartimage')

class SmartImageById(BrowserView):
    """Дать изображение по идентификатору"""
    __module__ = __name__
    implements(ISmartImageById)
    __name__ = '@@smartimagebyid'

    def __init__(self, context, request):
        super(SmartImageById, self).__init__(context, request)
        self.__parent__ = self.context = context

    def __getitem__(self, name):
        adapter = SmartImageContainerView(self, self.request)
        adapter.__name__ = name
        self.lastname = name
        return adapter

    def __contains__(self, name):
        return True

    def get(self, name, d):
        return [
         name]

    @property
    def title(self):
        return 'blablabla'