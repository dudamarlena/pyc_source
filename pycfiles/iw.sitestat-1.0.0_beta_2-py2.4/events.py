# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/events.py
# Compiled at: 2008-10-10 10:14:00
"""
Events handlers. See configure.zcml for bindings
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.component import queryAdapter, getAdapter
from iw.sitestat.interfaces import IContentOptions, ISitestatConfigSchema
from iw.sitestat.utils import getSite
from iw.sitestat.browser.contentoptions import compileClickinPaths
from iw.sitestat.config import PRODUCTNAME

def removeFromClickinsOnDelete(item, event):
    """Handles content removal if targetted by clickins"""
    qi = getSite().portal_quickinstaller
    if not qi.isProductInstalled(PRODUCTNAME):
        return
    options = queryAdapter(item, IContentOptions)
    if options is None:
        return
    if options.is_clickin_target:
        global_config = getAdapter(getSite(), ISitestatConfigSchema)
        clickin_uids = list(global_config.clickin_uids)
        clickin_uids.remove(item.UID())
        global_config.clickin_uids = clickin_uids
        compileClickinPaths()
    return


def updateClickinsOnMove(item, event):
    """Handles moves of clickin targetted items"""
    qi = getSite().portal_quickinstaller
    if not qi.isProductInstalled(PRODUCTNAME):
        return
    options = queryAdapter(item, IContentOptions)
    if options is None:
        return
    if options.is_clickin_target:
        compileClickinPaths()
    return