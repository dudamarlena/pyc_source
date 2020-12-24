# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/adapters/product_variants_management.py
# Compiled at: 2008-09-03 11:14:27
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariantsManagement

class ProductVariantsManagement:
    """Provides IProductVariantsManagement for product content objects.
    """
    __module__ = __name__
    implements(IProductVariantsManagement)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context

    def addVariants(self, properties, title='', article_id='', price=0.0):
        """
        """
        article_id = article_id.replace('%A', self.context.getArticleId())
        article_id = article_id.replace('%T', self.context.Title())
        title = title.replace('%A', self.context.getArticleId())
        title = title.replace('%T', self.context.Title())
        i = 0
        for properties in self._cartesian_product(*properties):
            if self.hasVariant(properties):
                continue
            i += 1
            new_article_id = article_id.replace('%N', str(i))
            new_title = title.replace('%N', str(i))
            new_id = self.context.generateUniqueId('ProductVariant')
            self.context.invokeFactory('ProductVariant', id=new_id, title=new_title, articleId=new_article_id, price=price, forProperties=properties)

    def deleteVariants(self, ids):
        """Deletes variants with given ids.
        """
        if not isinstance(ids, (list, tuple)):
            ids = (
             ids,)
        self.context.manage_delObjects(ids)

    def getDefaultVariant(self):
        """
        """
        try:
            return self.getVariants()[0]
        except IndexError:
            return

        return

    def getVariants(self):
        """
        """
        return self.context.objectValues('ProductVariant')

    def getSelectedVariant(self, selected_properties=None):
        """
        """
        if selected_properties is None:
            selected_properties = {}
            for (name, value) in self.context.REQUEST.items():
                if name.startswith('property'):
                    selected_properties[name[9:]] = value

        result = []
        for (key, value) in selected_properties.items():
            result.append('%s:%s' % (key, value))

        for variant in self.getVariants():
            found = True
            for selected_property in result:
                if selected_property not in variant.getForProperties():
                    found = False
                    break

            if found == True:
                return variant

        return

    def hasVariant(self, properties):
        """
        """
        properties.sort()
        for variant in self.getVariants():
            for_properties = list(variant.getForProperties())
            for_properties.sort()
            if properties == for_properties:
                return True

        return False

    def hasVariants(self):
        """
        """
        if len(self.getVariants()) > 0:
            return True
        else:
            return False

    def _cartesian_product(self, *seqin):
        """Calculates the cartesian product of given lists.
        """

        def rloop(seqin, comb):
            if seqin:
                for item in seqin[0]:
                    newcomb = comb + [item]
                    for item in rloop(seqin[1:], newcomb):
                        yield item

            else:
                yield comb

        return rloop(seqin, [])