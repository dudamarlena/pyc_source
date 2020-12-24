# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/setuphandlers.py
# Compiled at: 2018-04-05 17:11:05
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Return a list of non-installable profiles."""
        return [
         'collective.behavior.richpreview:uninstall']