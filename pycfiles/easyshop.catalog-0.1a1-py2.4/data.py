# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/adapters/data.py
# Compiled at: 2008-09-03 11:14:27
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariant
from easyshop.core.interfaces import IProductVariantsManagement

class ProductData(object):
    """An adapter which provides IData for product content objects.
    """
    __module__ = __name__
    implements(IData)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context

    def asDict(self):
        """
        """
        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants() == True:
            variant = pvm.getSelectedVariant() or pvm.getDefaultVariant()
            return IData(variant).asDict()
        else:
            cm = ICurrencyManagement(self.context)
            price = IPrices(self.context).getPriceForCustomer()
            price = cm.priceToString(price)
            image = IImageManagement(self.context).getMainImage()
            if image is not None:
                image = '%s/image_%s' % (image.absolute_url(), 'preview')
            images = []
            for temp in IImageManagement(self.context).getImages():
                images.append('%s/image_tile' % temp.absolute_url())

            return {'article_id': self.context.getArticleId(), 'title': self.context.Title(), 'short_title': self.context.getShortTitle() or self.context.Title(), 'description': self.context.Description(), 'url': self.context.absolute_url(), 'price': price, 'image': image, 'images': images, 'text': self.context.getText(), 'short_text': self.context.getShortText()}
        return


class ProductVariantData:
    """An adapter which provides IData for product variant content objects.
    """
    __module__ = __name__
    implements(IData)
    adapts(IProductVariant)

    def __init__(self, context):
        """
        """
        self.context = context
        self.parent = context.aq_inner.aq_parent

    def asDict(self):
        """
        """
        image = IImageManagement(self.context).getMainImage()
        if image is not None:
            image = '%s/image_%s' % (image.absolute_url(), 'preview')
        images = []
        for temp in IImageManagement(self.context).getImages():
            images.append('%s/image_tile' % temp.absolute_url())

        title = self.context.Title() or self.parent.Title()
        short_title = self.context.getShortTitle() or self.parent.getShortTitle() or title
        if '%' in short_title:
            short_title = short_title.replace('%P', self.parent.getShortTitle())
        article_id = self.context.getArticleId() or self.parent.getArticleId()
        if '%' in article_id:
            article_id = article_id.replace('%P', self.parent.getArticleId())
        text = self.context.getText() or self.parent.getText()
        if '%' in text:
            text = text.replace('%P', self.parent.getText())
        short_text = self.context.getShortText() or self.parent.getShortText()
        if '%' in short_text:
            short_text = short_text.replace('%P', self.parent.getShortText())
        description = self.context.Description() or self.parent.Description()
        if '%' in description:
            description = description.replace('%P', self.parent.Description())
        options = []
        for option in self.context.getForProperties():
            (name, value) = option.split(':')
            options.append({'name': name, 'value': value})

        return {'article_id': article_id, 'title': title, 'short_title': short_title, 'description': description, 'url': self.context.absolute_url(), 'image': image, 'images': images, 'text': text, 'short_text': short_text, 'options': options}