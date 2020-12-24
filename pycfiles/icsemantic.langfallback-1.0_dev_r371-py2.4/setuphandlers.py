# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/setuphandlers.py
# Compiled at: 2008-10-06 10:31:06
""" CMFDefault setup handlers.

$Id: setuphandlers.py 236 2008-06-10 20:28:23Z crocha $
"""
from StringIO import StringIO
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from icsemantic.core.interfaces import IContentTypesMultilingualPatcher

def patchPortalTypes(portal, out):
    """
    """
    archetype_tool = getToolByName(portal, 'archetype_tool')
    for atype in archetype_tool.listTypes():
        print >> out, 'Patching getters for %s' % atype
        if hasattr(atype, 'getLanguage'):
            ccpatcher = getUtility(IContentTypesMultilingualPatcher)
            ccpatcher.patch(atype)


def unpatchPortalTypes(portal, out):
    """
    """
    archetype_tool = getToolByName(portal, 'archetype_tool')
    for atype in archetype_tool.listTypes():
        if hasattr(atype, 'getLanguage'):
            ccpatcher = getUtility(IContentTypesMultilingualPatcher)
            ccpatcher.unpatch(atype)


def importVarious(context):
    """ Import various settings.

    This provisional handler will be removed again as soon as full handlers
    are implemented for these steps.
    """
    site = context.getSite()
    out = StringIO()
    logger = context.getLogger('icsemantic.langfallback')
    print >> out, 'Various settings imported.'
    logger.info(out.getvalue())
    return out.getvalue()


def unimportVarious(context):
    """ Import various settings.

    This provisional handler will be removed again as soon as full handlers
    are implemented for these steps.
    """
    site = context.getSite()
    return 'Various settings imported.'