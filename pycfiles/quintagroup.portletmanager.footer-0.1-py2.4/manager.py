# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/portletmanager/footer/manager.py
# Compiled at: 2009-10-06 10:29:36
from zope.interface import Interface
from zope.component import adapts
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.portlets.manager import ColumnPortletManagerRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from quintagroup.portletmanager.footer.interfaces import IFooter

class FooterPortletManagerRenderer(ColumnPortletManagerRenderer):
    """Render a footer portlets
    """
    __module__ = __name__
    adapts(Interface, IDefaultBrowserLayer, IBrowserView, IFooter)
    template = ViewPageTemplateFile('templates/portlets.pt')
    error_message = ViewPageTemplateFile('templates/error_message.pt')