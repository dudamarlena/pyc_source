# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/lbn/zenoss/browser/zensetup.py
# Compiled at: 2012-06-05 01:35:49
import logging, os, transaction, subprocess
from Acquisition import aq_base, aq_inner
from OFS.CopySupport import CopyError
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger('lbn.zenoss.zensetup')
from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.CmdBase import CmdBase
from Products.ZenModel.zenbuild import zenbuild
from Products.ZenRelations.ImportRM import ImportRM

def createZentinel(app, skipusers=True):
    """
    function to create a zport
    """
    try:
        zb = bzenbuild(app)
        zb.build()
        zport = app.zport
        if skipusers:
            zport.dmd._rq = True
    except:
        logger.error('Create Zentinel instance failed', exc_info=True)


class bzenbuild(zenbuild):
    """
    no command-line opts zenbuild
    """
    revertables = ('index_html', 'standard_error_message')

    def __init__(self, app):
        CmdBase.__init__(self, noopts=True)
        self.app = app

    def build(self):
        """
        don't let zenbuild trash default Zope
        """
        transaction.begin()
        app = self.app
        for id in self.revertables:
            if app.hasObject(id):
                try:
                    app.manage_renameObject(id, '%s.save' % id)
                except CopyError:
                    pass

        zenbuild.build(self)
        loader = ImportRM()
        directory = os.path.join(os.environ['ZENHOME'], 'Products', 'ZenModel', 'data')
        for file in os.listdir(directory):
            if not file.endswith('.xml'):
                continue
            loader.loadObjectFromXML(os.path.join(directory, file))

        std_err = aq_base(app._getOb('standard_error_message', None))
        if std_err:
            app.zport._setObject('standard_error_message', std_err)
        for id in self.revertables:
            if app.hasObject(id):
                app._delObject(id)
            try:
                app.manage_renameObject('%s.save' % id, id)
            except CopyError:
                pass

        transaction.commit()
        return


class ZenSetup(BrowserView):
    """
    Creates a Zenoss installation
    """

    def debug(self):
        """
        ensure product installed, placeholder to present installation info
        """
        return 'lbn.zenoss browser views are registered'

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
        MYSQL = 'mysql --user=root'
        for cmd in ('%s create database events' % MYSQL,
         '% events < %s/Products/ZenEvents/db/zenevents.sql' % (MYSQL, os.environ['ZENHOME']),
         '% events < %s/Products/ZenEvents/db/zenprocs.sql' % (MYSQL, os.environ['ZENHOME'])):
            try:
                pipe = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except OSError, e:
                raise OSError, '%s: %s' % (cmd, str(e))

        self.request.set('manage_tabs_message', 'created MySQL')
        self.request.redirect('manage_main')