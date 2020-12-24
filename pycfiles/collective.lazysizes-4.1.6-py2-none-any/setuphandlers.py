# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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