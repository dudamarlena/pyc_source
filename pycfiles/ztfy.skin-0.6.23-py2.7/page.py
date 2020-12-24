# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/page.py
# Compiled at: 2012-07-02 16:54:32
__docformat__ = 'restructuredtext'
from z3c.template.interfaces import ILayoutTemplate, IPageTemplate
from zope.publisher.interfaces.browser import IBrowserSkinType
from z3c.template.template import getPageTemplate, getLayoutTemplate
from zope.component import getMultiAdapter, getUtility, queryUtility
from zope.interface import implements
from zope.publisher.browser import BrowserPage
from zope.publisher.skinnable import applySkin
from ztfy.skin.interfaces import IBaseForm

class BaseTemplateBasedPage(BrowserPage):
    template = getPageTemplate()

    def update(self):
        pass

    def render(self):
        if self.template is None:
            template = getMultiAdapter((self, self.request), IPageTemplate)
            return template(self)
        else:
            return self.template()

    def __call__(self):
        self.update()
        return self.render()


class TemplateBasedPage(BaseTemplateBasedPage):
    layout = getLayoutTemplate()

    def __call__(self):
        self.update()
        if self.layout is None:
            layout = getMultiAdapter((self, self.request), ILayoutTemplate)
            return layout(self)
        else:
            return self.layout()


class BaseBackView(object):
    """Base back-office view, automatically selecting the good skin"""
    implements(IBaseForm)

    def update(self):
        skin = queryUtility(IBrowserSkinType, 'ZMI')
        if skin is None or skin is not None and not skin.providedBy(self.request):
            applySkin(self.request, getUtility(IBrowserSkinType, 'ZTFY.BO'))
        return