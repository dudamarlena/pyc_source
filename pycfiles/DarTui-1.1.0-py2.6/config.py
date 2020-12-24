# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dartui/config.py
# Compiled at: 2012-04-16 18:25:37
import os, sql, common, utils, actions

class ConfigDir:

    def __init__(self, config_path):
        self.config_path = os.path.abspath(config_path)
        if not os.path.isdir(self.config_path):
            os.makedirs(self.config_path)
        self._create_dirs()
        self.db_name = 'dartui.db'
        self.db_path = os.path.join(self.config_path, self.db_name)
        self.refresh()
        db = self.get_db()
        tables = db._get_tables()
        if 'settings' in tables and 'table_versions' not in tables:
            print 'old db style found, update settings table'
            update_settings_table = True
        else:
            update_settings_table = False
        self.table_versions = self.get_table_versions()
        for table in sql.tables:
            if table != 'table_versions' and table in self.table_versions:
                db = self.get_db(sql.tables[table])
                if sql.tables[table].version > self.table_versions[table]:
                    db.update_table_struct()
                elif table == 'settings' and update_settings_table:
                    db.update_table_struct()

    def _create_dirs(self):
        DIRS = ('torrent_cache', )
        for d in DIRS:
            dpath = os.path.join(self.config_path, d)
            if not os.path.isdir(dpath):
                print ('creating dir: {0}').format(dpath)
                os.mkdir(dpath)

    def get_table_versions(self):
        table_versions = {}
        db = self.get_db(sql.tables['table_versions'])
        db.insert_defaults()
        for row in db.get_table_contents():
            table_versions[row['name']] = row['version']

        return table_versions

    def has_db_conn(self):
        if self.db_conn is not None:
            return True
        else:
            return False
            return

    def _set_default_values(self):
        self.settings = {}
        self.rt = None
        return

    def update_settings(self, settings):
        settings['show_welcome'] = False
        db = self.get_db(sql.tables['settings'])
        db.update_table_contents(settings)
        self.refresh()

    def refresh(self):
        self._set_default_values()
        db = self.get_db(sql.tables['settings'])
        self.settings = db.get_table_contents()
        self.get_rt_connection()
        if self.rt is not None:
            self.settings['dest_path'] = self.rt.directory
            self.settings['upload_rate'] = self.rt.upload_rate
            self.settings['download_rate'] = self.rt.download_rate
        return

    def get_rt_url(self):
        self.rt_url = utils.build_url(self.settings['host'], self.settings['port'], self.settings['username'], self.settings['password'])
        return self.rt_url

    def get_rt_connection(self):
        self.rt = utils.get_rtorrent_connection(self.get_rt_url())
        self.tracker_cache = {}
        self.old_torrent_cache = []
        self.torrent_cache = []
        return self.rt

    def get_db(self, table_obj=None):
        return sql.Database(self.db_path, table_obj)

    def get_rt(self):
        return self.rt

    def is_local(self):
        """Checks if DarTui is running on the same system as rtorrent"""
        VALID_LOCAL_ADDRS = ('localhost', '127.0.0.1', '0.0.0.0')
        return self.settings['host'].lower() in VALID_LOCAL_ADDRS