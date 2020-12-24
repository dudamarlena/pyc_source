# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/portlets/formatter.py
# Compiled at: 2008-09-03 11:14:29
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from easyshop.core.config import _
from easyshop.core.config import TEXTS, TITLES, IMAGE_SIZES
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IFormatable
from easyshop.core.interfaces import IProductSelector
from easyshop.core.interfaces import IShop

class IFormatterPortlet(IPortletDataProvider):
    """
    """
    __module__ = __name__


class Assignment(base.Assignment):
    """
    """
    __module__ = __name__
    implements(IFormatterPortlet)

    def __init__(self):
        """
        """
        pass

    @property
    def title(self):
        """
        """
        return _('EasyShop: Formatter')


class Renderer(base.Renderer):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('formatter.pt')

    @property
    def available(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        if not mtool.checkPermission('Manage portal', self.context):
            return False
        if IFormatable.providedBy(self.context) == False:
            return False
        return True

    @memoize
    def getFormatInfo(self):
        """
        """
        fi = IFormats(self.context)
        return fi.getFormats(effective=False)

    def getTitles(self):
        """
        """
        fi = self.getFormatInfo()
        selected_title = fi['title']
        result = []
        for title in TITLES:
            result.append({'id': title[0], 'title': title[1], 'selected': selected_title == title[0]})

        return result

    def getTexts(self):
        """
        """
        fi = self.getFormatInfo()
        selected_text = fi['text']
        result = []
        for text in TEXTS:
            result.append({'id': text[0], 'title': text[1], 'selected': selected_text == text[0]})

        return result

    def getImageSizes(self):
        """
        """
        fi = self.getFormatInfo()
        selected_size = fi['image_size']
        sizes = IMAGE_SIZES.keys()
        sizes.sort(lambda a, b: cmp(IMAGE_SIZES[a][0], IMAGE_SIZES[b][0]))
        result = []
        for size in sizes:
            result.append({'title': size, 'selected': selected_size == size})

        return result

    @memoize
    def showEnabledField(self):
        """Returns True when the enabled field should be displayed.
        """
        if IShop.providedBy(self.context) == True:
            return False
        else:
            return True

    @memoize
    def showLinesPerPage(self):
        """Returns True when the lines per page field should be displayed.
        """
        if IProductSelector.providedBy(self.context) == True:
            return False
        else:
            return True


class AddForm(base.NullAddForm):
    """
    """
    __module__ = __name__

    def create(self):
        """
        """
        return Assignment()


class FormatterView(BrowserView):
    """
    """
    __module__ = __name__

    def saveFormatter(self):
        """
        """
        fi = IFormats(self.context)
        f = fi.setFormats(self.request)
        referer = self.request.get('HTTP_REFERER', '')
        if referer.find('thank-you') != -1:
            url = referer
        else:
            url = self.context.absolute_url()
        self.request.response.redirect(url)