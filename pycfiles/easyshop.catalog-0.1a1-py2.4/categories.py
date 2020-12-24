# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/viewlets/categories.py
# Compiled at: 2008-09-03 11:14:26
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IShopManagement

class CategoriesViewlet(ViewletBase):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('categories.pt')

    def getCategories(self):
        """
        """
        f = self.getFormats()
        products_per_line = f.get('products_per_line')
        cm = ICategoryManagement(self.context)
        line = []
        lines = []
        for (i, category) in enumerate(cm.getTopLevelCategories()):
            if len(category.getImage()) != 0:
                image_url = '%s/image_%s' % (category.absolute_url(), f.get('image_size'))
            else:
                image_url = None
            temp = f.get('text')
            if temp == 'description':
                text = category.getDescription()
            elif temp == 'short_text':
                text = category.getShortText()
            elif temp == 'text':
                text = category.getText()
            else:
                text = ''
            if (i + 1) % products_per_line == 0:
                klass = 'last'
            else:
                klass = 'notlast'
            line.append({'title': category.Title(), 'text': text, 'url': category.absolute_url(), 'image_url': image_url, 'klass': klass})
            if (i + 1) % products_per_line == 0:
                lines.append(line)
                line = []

        if len(line) > 0:
            lines.append(line)
        return lines

    @memoize
    def getBackToOverViewUrl(self):
        """
        """
        if IShop.providedBy(self.context):
            return
        parent_category = self.context.getRefs('parent_category')
        if len(parent_category) > 0:
            return parent_category[0].absolute_url()
        shop = IShopManagement(self.context).getShop()
        return shop.absolute_url()

    @memoize
    def getFormats(self):
        """
        """
        return IFormats(self.context).getFormats()

    @memoize
    def getTdWidth(self):
        """
        """
        return '%s%%' % (100 / self.getFormats().get('products_per_line'))