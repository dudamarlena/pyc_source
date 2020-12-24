# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/transform/docbook/setuphandlers.py
# Compiled at: 2009-03-11 15:34:26
from Products.CMFCore.utils import getToolByName

def registerMimetype(portal):
    """Add application/docbook+xml to the mimetype registry"""
    mime_reg = getToolByName(portal, 'mimetypes_registry')
    if not mime_reg.lookup('application/docbook+xml'):
        mime_reg.manage_addMimeType('DocBook', [
         'application/docbook+xml'], None, 'text.png')
    return


def uninstallMimetype(portal):
    """Delete the docbook mimetype"""
    mime_reg = getToolByName(portal, 'mimetypes_registry')
    if 'application/docbook+xml' in mime_reg.objectIds():
        mime_reg.manage_delObjects(['application/docbook+xml'])


def installTransform(portal):
    """"""
    transforms = getToolByName(portal, 'portal_transforms')
    if 'html_to_docbook' not in transforms.objectIds():
        transforms.manage_addTransform('html_to_docbook', 'collective.transform.docbook.html_to_docbook')


def uninstallTransform(portal):
    """"""
    transforms = getToolByName(portal, 'portal_transforms')
    if 'html_to_docbook' in transforms.objectIds():
        transforms.manage_delObjects(['html_to_docbook'])


def importVarious(context):
    """Various import step code"""
    marker_file = 'collective.transform.docbook-default.txt'
    if context.readDataFile(marker_file) is None:
        return
    portal = context.getSite()
    registerMimetype(portal)
    installTransform(portal)
    return


def importVariousUninstall(context):
    """Various uninstall step code"""
    marker_file = 'collective.transform.docbook-uninstall.txt'
    if context.readDataFile(marker_file) is None:
        return
    portal = context.getSite()
    uninstallMimetype(portal)
    uninstallTransform(portal)
    return