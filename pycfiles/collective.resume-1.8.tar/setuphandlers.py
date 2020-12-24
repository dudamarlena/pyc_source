# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/collective/resume/setuphandlers.py
# Compiled at: 2019-09-08 03:34:04
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
         'collective.resume:uninstall']


def post_install(context):
    """Post install script"""
    pass


def uninstall(context):
    """Uninstall script"""
    pass