# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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