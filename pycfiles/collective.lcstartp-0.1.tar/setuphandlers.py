# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/setuphandlers.py
# Compiled at: 2018-10-17 10:19:27
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool import interfaces as BBB
from zope.interface import implementer

@implementer(BBB.INonInstallable)
@implementer(INonInstallable)
class NonInstallable(object):

    @staticmethod
    def getNonInstallableProducts():
        """Hide in the add-ons configlet."""
        return [
         'collective.lazysizes.upgrades.v10']

    @staticmethod
    def getNonInstallableProfiles():
        """Hide at site creation."""
        return [
         'collective.lazysizes.upgrades.v10:default',
         'collective.lazysizes:uninstall']