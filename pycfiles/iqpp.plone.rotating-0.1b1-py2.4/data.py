# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/iqpp/plone/rotating/adapters/data.py
# Compiled at: 2008-08-03 12:08:42
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts
from Products.ATContentTypes.interface import IATDocument
from Products.ATContentTypes.interface import IATImage
from iqpp.plone.rotating.interfaces import IData

class Data:
    """Base adapter, which provides IData for arbitrary objects.
    """
    __module__ = __name__
    implements(IData)
    adapts(Interface)

    def __init__(self, context):
        """
        """
        self.context = context

    def getContent(self):
        """
        """
        return self.context.Description()

    def getFooter(self):
        """
        """
        return

    def getTitle(self):
        """
        """
        return self.context.Title()

    def getURL(self):
        """
        """
        return self.context.absolute_url()


class ImageData(Data):
    """Adapter, which provides IData for ATDocuments.
    """
    __module__ = __name__
    implements(IData)
    adapts(IATImage)

    def getContent(self):
        """
        """
        return self.context.getTag()