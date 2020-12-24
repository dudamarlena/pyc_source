# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/Extensions/Install.py
# Compiled at: 2009-04-26 22:17:24
from Products.CMFCore.utils import getToolByName
from Products.DigestoContentTypes.utilities.interfaces import INormativaTypes
from Products.DigestoContentTypes.utilities.types import NormativaTypes

def afterInstall(self, reinstall, product):
    portal = getToolByName(self, 'portal_url').getPortalObject()
    sm = portal.getSiteManager()
    if not sm.queryUtility(INormativaTypes):
        sm.registerUtility(NormativaTypes(), INormativaTypes)
        nt = sm.getUtility(INormativaTypes)
        nt.types = ['Ley', 'Ordenanza', 'Decreto', unicode('Resolución', 'utf-8')]
    portal_setup = getToolByName(self, 'portal_setup')
    profile = 'profile-Products.DigestoContentTypes:extra'
    portal_setup.runAllImportStepsFromProfile(profile)