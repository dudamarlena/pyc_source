# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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