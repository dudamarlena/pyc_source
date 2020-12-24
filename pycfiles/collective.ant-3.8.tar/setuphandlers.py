# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/collective/ant/setuphandlers.py
# Compiled at: 2019-09-07 22:16:15
from Products.CMFPlone.interfaces import INonInstallable
from plone import api
from plone.portlets.interfaces import IPortletAssignmentSettings
from zope.interface import implementer

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
         'collective.ant:uninstall']


def post_install(context):
    """Post install script"""
    portal = context.__parent__
    del_default_content(portal)


def uninstall(context):
    """Uninstall script"""
    pass


def del_default_content(context):
    if 'news' in context:
        api.content.delete(context['news'])
    if 'events' in context:
        api.content.delete(context['events'])
    if 'Members' in context:
        api.content.delete(context['Members'])
    if 'front-page' in context:
        api.content.delete(context['front-page'])