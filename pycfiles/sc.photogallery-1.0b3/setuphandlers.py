# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/setuphandlers.py
# Compiled at: 2017-10-20 17:03:39
from Products.CMFPlone import interfaces as Plone
from Products.CMFQuickInstallerTool import interfaces as QuickInstaller
from zope.interface import implementer

@implementer(Plone.INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
         'sc.photogallery:uninstall',
         'sc.photogallery.upgrades.v1001:default']


@implementer(QuickInstaller.INonInstallable)
class HiddenProducts(object):

    def getNonInstallableProducts(self):
        """Do not show on QuickInstaller's list of installable products."""
        return [
         'sc.photogallery.upgrades.v1001']