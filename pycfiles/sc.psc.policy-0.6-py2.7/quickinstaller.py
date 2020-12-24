# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sc/psc/policy/quickinstaller.py
# Compiled at: 2012-07-17 18:10:20
from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonInstallableProducts
from Products.CMFPlone.interfaces import INonInstallable as INonInstallableProfiles
from sc.psc.policy.config import PRODUCTS

def nonInstallableProducts(products):
    """ Given a list of product tuples formated as
        (name,locked,hidden,install,profile,runProfile)
        we return a list of names to be used by HiddenProducts
    """
    pNames = [ name for name, locked, hidden, install, profile, runProfile in products if hidden
             ]
    pOldStyle = [ name.replace('Products.', '') for name in pNames if name.startswith('Products.')
                ]
    pNames = pOldStyle + pNames
    return pNames


def nonInstallableProfiles(products):
    """ Given a list of product tuples formated as
        (name,locked,hidden,install,profile,runProfile)
        we return a list of names to be used by HiddenProfiles
    """
    pNames = [ profile for name, locked, hidden, install, profile, runProfile in products if hidden
             ]
    return pNames


class HiddenProducts(object):
    implements(INonInstallableProducts)

    def getNonInstallableProducts(self):
        return nonInstallableProducts(PRODUCTS)


class HiddenProfiles(object):
    implements(INonInstallableProfiles)

    def getNonInstallableProfiles(self):
        return nonInstallableProfiles(PRODUCTS)