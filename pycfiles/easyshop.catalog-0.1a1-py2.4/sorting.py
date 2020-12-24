# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/portlets/sorting.py
# Compiled at: 2008-09-03 11:14:29
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from easyshop.core.config import _
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import IProduct

class ISortingPortlet(IPortletDataProvider):
    """
    """
    __module__ = __name__


class Assignment(base.Assignment):
    """
    """
    __module__ = __name__
    implements(ISortingPortlet)

    def __init__(self):
        """
        """
        pass

    @property
    def title(self):
        """
        """
        return _('EasyShop: Sorting')


class Renderer(base.Renderer):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('sorting.pt')

    @property
    def available(self):
        """
        """
        return True


class AddForm(base.NullAddForm):
    """
    """
    __module__ = __name__

    def create(self):
        """
        """
        return Assignment()


from Products.Five.browser import BrowserView

class SortingPortletView(BrowserView):
    """
    """
    __module__ = __name__

    def setSorting(self):
        """
        """
        sorting = self.request.get('sorting')
        self.request.SESSION['sorting'] = sorting
        url = self.context.absolute_url()
        self.request.response.redirect(url)