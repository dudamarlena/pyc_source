# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/setuphandlers.py
# Compiled at: 2011-01-11 16:22:56
from Acquisition import aq_inner
from config import SKINS_DIR, GLOBALS
from lbn.zenoss.packutils import _addSkin

def install(context):
    portal = context.getSite()
    portal.portal_quickinstaller.installProduct('windowZ')
    portal.portal_windowZ.update(dynamic_window=True)
    zport = aq_inner(portal.aq_parent).zport
    _addSkin(zport.portal_skins, SKINS_DIR, 'bastionzport', GLOBALS)


def uninstall(context):
    portal = context.getSite()