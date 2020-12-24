# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thet-data/data/dev/htu/bda.htu.buildout/src/collective.teaser/collective/teaser/browser/manager.py
# Compiled at: 2013-03-13 08:34:51
from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.portlets.manager import ColumnPortletManagerRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.teaser.interfaces import ITeaserPortletManager

class TeaserPortletManagerRenderer(ColumnPortletManagerRenderer):
    adapts(Interface, IDefaultBrowserLayer, IBrowserView, ITeaserPortletManager)
    template = ViewPageTemplateFile('teaser_portlet_manager_renderer.pt')