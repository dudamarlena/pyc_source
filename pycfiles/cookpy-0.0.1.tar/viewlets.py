# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cooking/theme/browser/viewlets.py
# Compiled at: 2010-08-12 16:17:02
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from Products.CMFPlone.utils import safe_unicode
from cgi import escape

class SimpleTitleViewlet(common.TitleViewlet):
    __module__ = __name__

    def index(self):
        portal_title = safe_unicode(self.portal_title())
        page_title = safe_unicode(self.page_title())
        return '<title>%s</title>' % escape(portal_title)


class SiteTitleViewlet(common.ViewletBase):
    """A custom version of the path bar (breadcrumbs) viewlet, which
    uses slightly different markup.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('templates/site_title.pt')


class SiteDomainViewlet(common.ViewletBase):
    """A viewlet to display current site domain name"""
    __module__ = __name__
    render = ViewPageTemplateFile('templates/site_domain.pt')


class SiteHeaderViewlet(common.ViewletBase):
    """A custom version of the path bar (breadcrumbs) viewlet, which
    uses slightly different markup.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('templates/site_header.pt')