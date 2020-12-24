# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mediawiki/setuphandlers.py
# Compiled at: 2008-10-06 10:31:13
""" iccommunity.mediawiki setup handlers.
"""
from StringIO import StringIO
from zope.interface import alsoProvides, directlyProvides, directlyProvidedBy
from zope.component import getUtility
from zope.app.component.hooks import setSite
from zope.app.component.interfaces import ISite, IPossibleSite
from Products.CMFCore.utils import getToolByName
from Products.Five.site.localsite import enableLocalSiteHook
import interfaces
from preferences import icCommunityManagementMediawikiRolesMapper, icCommunityManagementMediawikiSQLServer
from config import HAS_PLONE3
from config import DEPENDENCIES
import transaction

def setup_site(context):
    """Site setup"""
    sm = context.getSiteManager()
    if not sm.queryUtility(interfaces.IicCommunityManagementMediawikiRolesMapper, name='iccommunity.configuration'):
        if HAS_PLONE3:
            sm.registerUtility(icCommunityManagementMediawikiRolesMapper(), interfaces.IicCommunityManagementMediawikiRolesMapper, 'iccommunity.configuration')
        else:
            sm.registerUtility(interfaces.IicCommunityManagementMediawikiRolesMapper, icCommunityManagementMediawikiRolesMapper(), 'iccommunity.configuration')
    if not sm.queryUtility(interfaces.IicCommunityManagementMediawikiSQLServer, name='iccommunity.configuration'):
        if HAS_PLONE3:
            sm.registerUtility(icCommunityManagementMediawikiSQLServer(), interfaces.IicCommunityManagementMediawikiSQLServer, 'iccommunity.configuration')
        else:
            sm.registerUtility(interfaces.IicCommunityManagementMediawikiSQLServer, icCommunityManagementMediawikiSQLServer(), 'iccommunity.configuration')


def setup_various(context):
    """Import various settings.

  This provisional handler will be removed again as soon as full handlers
  are implemented for these steps.
  """
    site = context.getSite()
    setup_site(site)