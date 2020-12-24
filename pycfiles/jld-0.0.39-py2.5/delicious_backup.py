# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\backup\delicious_backup.py
# Compiled at: 2009-01-13 14:40:52
""" Backup for Delicious bookmarks
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: delicious_backup.py 795 2009-01-13 19:42:53Z JeanLou.Dupont $'
__msgs__ = [
 'error_init_folder', 'error_create_folder', 'error_cant_write']
import sys, os, logging, datetime, urllib2
from stat import *
import jld.api as api
from jld.cmd import BaseCmd
import jld.registry as reg, jld.tools.mos as mos, jld.api.delicious as dlc, jld.backup.delicious_messages as msg, jld.backup.delicious_printer as printer, jld.backup.delicious_db as db

class Backup(BaseCmd):
    """Delicious Backup class
    """
    _regDomain = 'delicious'
    _configParams = [
     'username', 'password', 'db_path']

    def __init__(self):
        BaseCmd.__init__(self)
        self.delicious = None
        self.logger = None
        self.quiet = False
        self.db_path = None
        self.db = None
        self.username = None
        self.password = None
        self.msgs = msg.Delicious_Messages()
        self.r = reg.Registry()
        return

    def cmd_listconfig(self, *args):
        """Lists the configuration"""
        pp = printer.Delicious_Printer_Config(self.msgs, self)
        if not self.quiet:
            pp.run(self)

    def cmd_llatest(self, *args):
        """Displays the latest update timestamp recorded in the database (logged)"""
        self._validateAuthParams()
        last = self._llatest()
        if not self.quiet:
            msg = self.msgs.render('report_local_update', {'time': last})
            self.logger.info(msg)

    def cmd_rlatest(self, *args):
        """Displays the latest update timestamp from Delicious"""
        self._validateAuthParams()
        self._initDelicious()
        last = self.delicious.getLastUpdate()
        if not self.quiet:
            msg = self.msgs.render('report_remote_update', {'time': last[0]})
            print msg

    def cmd_updatedb(self, *args):
        """Updates the local database with the most recent entries (logged)"""
        remote = self._getRemoteUpdate()
        if not self._shouldUpdate(remote):
            msg = self.msgs.render('report_update_none')
            self.logger.info(msg)
            return
        posts = self.delicious.getRecentPosts()
        self._doUpdate(posts, remote, 'report_updatedb', False)

    def cmd_updatedbfull(self, *args):
        """ Updates the local database with complete remote data (logged)"""
        remote = self._getRemoteUpdate()
        if not self._shouldUpdate(remote):
            msg = self.msgs.render('report_update_none')
            self.logger.info(msg)
            return
        posts = self.delicious.getPostsAll()
        self._doUpdate(posts, remote, 'report_updatedbfull')

    def cmd_listdb(self, *args):
        """ Lists the current entries in the database, optional filter by tag"""
        try:
            tag = args[0]
        except:
            tag = None

        self._initDb()
        all = db.Posts.getAll(tag)
        pp = printer.Delicious_Printer_Posts(self.msgs)
        if not self.quiet:
            pp.run(all)
            print 'total[%s]' % str(len(all))
        return

    def cmd_deletedb(self, *args):
        """Deletes the database"""
        self._deleteDb()

    def _doUpdate(self, list, remote, msg, record_last=True):
        """ Performs an update cycle """
        (total, updated, created) = db.Posts.updateFromList(list)
        if record_last:
            db.Updates.update(self.username, remote)
        if not self.quiet:
            msg = self.msgs.render(msg, {'total': total, 'updated': updated, 'created': created})
            self.logger.info(msg)

    def _getRemoteUpdate(self):
        """ Gets the remote update status """
        try:
            remote = self._rlatest()[0]
        except:
            remote = None

        return remote

    def _shouldUpdate(self, remote):
        """ Verifies if an update is in order """
        local = self._llatest()
        return local != remote

    def _llatest(self):
        """ Local Last Update"""
        self._initDb()
        last = db.Updates.getLatest(self.username)
        return last

    def _rlatest(self):
        """ Remote Last Update """
        self._validateAuthParams()
        self._initDelicious()
        currentUpdate = self.delicious.getLastUpdate()
        return currentUpdate

    def _validateAuthParams(self):
        """ Performs basic validation of the authentication parameters """
        if not self.username:
            raise api.ErrorConfig('', {'param': 'username'})
        if not self.password:
            raise api.ErrorConfig('', {'param': 'password'})

    def _deleteDb(self):
        path = mos.replaceHome(self.db_path)
        db.Db.deleteDb(path)

    def _initDelicious(self):
        if self.delicious is None:
            self.delicious = dlc.Client(self.username, self.password)
        return

    def _initDb(self):
        if self.db is None:
            path = mos.replaceHome(self.db_path)
            self.db = db.Db(path)
        return