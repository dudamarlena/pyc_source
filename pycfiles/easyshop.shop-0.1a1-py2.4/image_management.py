# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/adapters/image_management.py
# Compiled at: 2008-09-03 11:15:25
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IProductVariant

class ImageManagement:
    """Provides IImageManagement for several classes.
    """
    __module__ = __name__
    implements(IImageManagement)

    def __init__(self, context):
        """
        """
        self.context = context

    def getMainImage(self):
        """Returns the main image. This is either the product itself or the 
        first image object within the product.
        """
        image = self.context.getField('image').get(self.context)
        if len(image) != 0:
            return self.context
        else:
            try:
                return self.context.objectValues('EasyShopImage')[0]
            except IndexError:
                return

        return

    def getImages(self):
        """Returns all images.
        """
        result = []
        image = self.context.getField('image').get(self.context)
        if len(image) != 0:
            result.append(self.context)
        result.extend(self.context.objectValues('EasyShopImage'))
        return result

    def hasImages(self):
        """Returns True if at least one image exists.
        """
        return len(self.getImages()) > 0


class ProductVariantImageManagement:
    """Provides IImageManagement for ProductVariant.
    """
    __module__ = __name__
    implements(IImageManagement)
    adapts(IProductVariant)

    def __init__(self, context):
        """
        """
        self.context = context
        self.parent = context.aq_inner.aq_parent

    def getMainImage(self):
        """Returns the main image. This is either the product itself or the
        first image object within the product.
        """
        image = self.context.getField('image').get(self.context)
        if len(image) == 0:
            image = self.parent.getField('image').get(self.parent)
        if len(image) != 0:
            return image
        images = self.context.objectValues('EasyShopImage')
        if len(images) == 0:
            images = self.parent.objectValues('EasyShopImage')
        if len(images) != 0:
            return images[0]
        return

    def getImages(self):
        """Returns all images.
        """
        result = []
        image = self.getMainImage()
        if image is not None:
            result.append(self.context)
        images = self.context.objectValues('EasyShopImage')
        if len(images) == 0:
            images = self.parent.objectValues('EasyShopImage')
        result.extend(images)
        return result

    def hasImages(self):
        """Returns True if at least one image exists.
        """
        return len(self.getImages()) > 0