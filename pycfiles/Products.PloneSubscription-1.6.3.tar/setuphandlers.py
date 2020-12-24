# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneStatCounter\setuphandlers.py
# Compiled at: 2008-07-07 10:54:58
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.publisher.interfaces.browser import IBrowserView
from zope.viewlet.interfaces import IViewlet
from plone.app.layout.viewlets.interfaces import IPortalFooter
from interfaces import IStatCounterConfig
from utility import StatCounterConfig
from utility import UTILITY_NAME
from viewlets import StatCounterViewlet

def importFinalSteps(context):
    """Install PloneStatCounter.
    """
    portal = context.getSite()
    addLocalUtility(portal)
    addViewlet(portal)


def addLocalUtility(portal):
    sm = portal.getSiteManager()
    if not sm.queryUtility(IStatCounterConfig, name=UTILITY_NAME):
        sm.registerUtility(StatCounterConfig(), IStatCounterConfig, UTILITY_NAME)


def addViewlet(portal):
    """Add the viewlet here (rather than in ZCML) so that it is only available
    when the local utility has been installed.
    """
    sm = portal.getSiteManager()
    sm.registerAdapter(StatCounterViewlet, (
     Interface, IDefaultBrowserLayer, IBrowserView, IPortalFooter), provided=IViewlet, name='PloneStatCounter.statcounter')