# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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