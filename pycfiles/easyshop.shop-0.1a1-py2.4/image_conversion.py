# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/adapters/image_conversion.py
# Compiled at: 2008-09-03 11:15:25
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import IImageConversion

class ImageConversion:
    """Dummy adapter to convert image before saving. 
    
    3rd-party developers can provide their own adapter to convert/add images
    before they are saved. See a example in DemmelhuberShop.
    """
    __module__ = __name__
    implements(IImageConversion)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def convertImage(self, data):
        """
        """
        return data