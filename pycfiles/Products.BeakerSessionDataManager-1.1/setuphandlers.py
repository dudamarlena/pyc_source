# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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