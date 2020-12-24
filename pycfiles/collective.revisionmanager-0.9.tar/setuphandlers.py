# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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