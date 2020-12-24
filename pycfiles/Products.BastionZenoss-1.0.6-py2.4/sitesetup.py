# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/browser/sitesetup.py
# Compiled at: 2011-01-11 16:22:56
import logging
from Acquisition import aq_base, aq_inner
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.CmdBase import CmdBase
from Products.ZenModel.zenbuild import zenbuild
from Products.BastionZenoss.config import *
from lbn.zenoss.packutils import _addSkin
import Products.CMFPlone, Products.GenericSetup
from Products.CMFPlone.factory import _DEFAULT_PROFILE, addPloneSite
from Products.GenericSetup.registry import _profile_registry
logger = logging.getLogger('BastionZenoss.sitesetup')

def createPlone(context):
    """
    funtion to create a Plone site
    """
    try:
        if not _profile_registry._profile_info.has_key(_DEFAULT_PROFILE):
            from Products.Five import zcml
            zcml.load_config('configure.zcml', Products.GenericSetup)
            zcml.load_config('configure.zcml', Products.CMFPlone)
        addPloneSite(context, 'plone', title='ZenPlone Portal')
        context.plone.portal_quickinstaller.installProduct('Products.BastionZenoss')
    except:
        logger.error('Create Plone instance failed', exc_info=True)


def createZentinel(context, skipusers=True):
    """
    function to create a zport
    """
    try:
        zb = bzenbuild(context)
        zb.build()
        zport = context.zport
        skinstool = zport.portal_skins
        _addSkin(skinstool, 'skins', 'lbn.zenoss', GLOBALS)
        if skipusers:
            zport.dmd._rq = True
    except:
        logger.error('Create Zentinel instance failed', exc_info=True)


class bzenbuild(zenbuild):
    """
    no command-line opts zenbuild
    """
    __module__ = __name__
    revertables = ('index_html', 'standard_error_message')

    def __init__(self, context):
        CmdBase.__init__(self, noopts=True)
        self.app = context.getPhysicalRoot()

    def build(self):
        """
        don't let zenbuild trash default Zope
        """
        app = self.app
        for id in self.revertables:
            if app.hasObject(id):
                app.manage_renameObject(id, '%s.save' % id)

        zenbuild.build(self)
        std_err = aq_base(app._getOb('standard_error_message'))
        app.zport._setObject('standard_error_message', std_err)
        for id in self.revertables:
            if app.hasObject(id):
                app._delObject(id)
            app.manage_renameObject('%s.save' % id, id)


class SiteSetup(BrowserView):
    """
    Creates a Zenoss installation
    """
    __module__ = __name__

    def createZentinel(self, skipusers=True):
        """
        creates zport, DMD in install root
        """
        context = aq_inner(self.context)
        createZentinel(context, skipusers)
        self.request.set('manage_tabs_message', 'created zenoss dmd')
        self.request.RESPONSE.redirect('zport/dmd')

    def createMySql(self):
        """
        setup (local) MySQL for Events processing
        """
        self.request.set('manage_tabs_message', 'created MySQL')
        self.request.redirect('manage_main')