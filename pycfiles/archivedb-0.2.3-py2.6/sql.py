# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/archivedb/sql.py
# Compiled at: 2011-12-26 16:36:16
import os, sys, re, pymysql, logging, archivedb.config as config
from archivedb.common import enum_to_list, list_to_enum, split_path

class DatabaseConnection():

    def __init__(self, host, user, passwd, database, port, table_name):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.port = port
        self.table_name = table_name
        self.table_struct = config.args['table_struct'][table_name]
        self.create_connection()

    def _check_connection(self):
        reconnect = False
        try:
            if self.db.ping() == False:
                reconnect = True
        except pymysql.err.OperationalError:
            reconnect = True

        if reconnect:
            log.warning('lost connection to database, reconnecting.')
            self.create_connection()

    def table_exists(self, table_name):
        self._check_connection()
        self.c.execute('SHOW TABLES')
        tables = self.c.fetchall()
        tables = [ t[0] for t in tables ]
        if table_name in tables:
            return True
        else:
            return False

    def create_database(self):
        db = pymysql.connect(self.host, self.user, self.passwd, port=self.port)
        c = db.cursor()
        c.execute(('CREATE DATABASE IF NOT EXISTS `{0}`').format(self.database))
        log.info(("database '{0}' created").format(self.database))

    def create_table(self, query):
        self._check_connection()
        self._execute(query)
        log.info('table created')

    def create_connection(self):
        try:
            self.db = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.database, port=self.port)
            self.c = self.db.cursor()
            log.debug('MySQL connection successful')
        except (pymysql.OperationalError, pymysql.InternalError), e:
            error_code = e.args[0]
            if error_code == 1049:
                log.info(("database '{0}' not found, creating.").format(self.database))
                self.create_database()
                self.create_conn()
            else:
                log.critical(('error when trying to connect to db: {0}').format(e))
                log.critical('closing thread')
                sys.exit(1)

    def insert_file(self, watch_dir, path, filename, md5, mtime, size):
        self._check_connection()
        query = ('INSERT INTO `{0}` (watch_dir, path, filename, md5, mtime, size) \n        VALUES %s').format(self.table_name)
        args = (
         (
          watch_dir,
          path,
          filename,
          md5,
          mtime,
          size),)
        self._execute(query, args)

    def update_file(self, watch_dir, path, filename, md5, mtime, size):
        self._check_connection()
        query = ('UPDATE `{0}` SET `md5` = %s, `mtime` = %s, `size` = %s\n                WHERE `watch_dir` = %s and `path` = %s \n                and `filename` = %s').format(self.table_name)
        args = (
         md5,
         mtime,
         size,
         watch_dir,
         path,
         filename)
        return self._execute(query, args)

    def move_file(self, src, dest):
        self._check_connection()
        query = ('UPDATE `{0}` SET `watch_dir` = %s, path = %s,\n                 filename = %s WHERE `watch_dir` = %s and `path` = %s \n                 and filename = %s').format(self.table_name)
        args = (
         dest[0], dest[1], dest[2],
         src[0], src[1], src[2])
        return self._execute(query, args)

    def delete_file(self, full_path):
        (watch_dir, path, filename) = split_path(config.args['watch_dirs'], full_path)
        data = self.get_fields(watch_dir, path, filename, ['id'])
        if data:
            id = data[0][0]
            log.info(('removing {0} from the database.').format(filename))
            self.delete_id(id)
        else:
            log.debug(("file '{0}' not found in database.").format(full_path))

    def delete_id(self, id):
        self._check_connection()
        query = 'DELETE FROM `archive` WHERE id = %s'
        args = id
        return self._execute(query, args)

    def delete_directory(self, d):
        self._check_connection()
        d = d.rstrip(os.sep) + os.sep
        (watch_dir, path) = split_path(config.args['watch_dirs'], d)[0:2]
        query = ('DELETE FROM `{0}` WHERE `watch_dir` = %s and\n                `path` REGEXP %s').format(self.table_name)
        args = (
         watch_dir,
         re.escape(path) + '(\\/|$)')
        return self._execute(query, args)

    def move_directory(self, src, dest):
        self._check_connection()
        src_watch_dir = src[0]
        dest_watch_dir = dest[0]
        src_path = src[1]
        dest_path = dest[1]
        query = ('SELECT `id`, `path` FROM `{0}` WHERE `path` \n                REGEXP %s').format(self.table_name)
        args = re.escape(src_path) + '(\\/|$)'
        self._execute(query, args)
        rows_changed = 0
        temp_c = self.db.cursor()
        data = self.c.fetchone()
        while data:
            id = data[0]
            old_path = data[1]
            new_path = old_path.replace(src_path, dest_path).strip(os.sep)
            query = ('UPDATE `{0}` SET `watch_dir` = %s, `path` = %s \n                    WHERE `id` = %s').format(self.table_name)
            args = (
             dest_watch_dir,
             new_path,
             id)
            rows_changed += self._execute(query, args, c=temp_c)
            data = self.c.fetchone()

        return rows_changed

    def get_fields(self, watch_dir, path, filename, fields):
        self._check_connection()
        if isinstance(fields, str):
            fields = [fields]
        fields = ('{0}').format(('`,`').join(fields))
        query = ('SELECT `{0}` FROM `{1}` WHERE watch_dir = %s and path = %s\n                and filename = %s').format(fields, self.table_name)
        args = (
         watch_dir, path, filename)
        if self._execute(query, args) == 0:
            return
        else:
            return self.c.fetchall()
            return

    def get_enum(self, field_index=1):
        self._check_connection()
        self._execute(('DESCRIBE `{0}`').format(self.table_name))
        enum_line = self.c.fetchall()[field_index][1]
        watch_list = enum_to_list(enum_line)
        return watch_list

    def alter_enum(self, field_name, watch_dirs):
        self._check_connection()
        query = ('ALTER TABLE `{0}` MODIFY `{1}` {2}').format(self.table_name, field_name, list_to_enum(watch_dirs))
        self._execute(query)

    def _execute(self, query, args=None, c=None):
        """Returns number of rows affected"""
        if c == None:
            c = self.c
        log.debug(('query = {0}').format(query))
        log.debug(('args = {0}').format(args))
        rows_affected = c.execute(query, args)
        log.debug(('rows_affected = {0}').format(rows_affected))
        return rows_affected

    def _query(self, query, args=None, c=None):
        """Returns all rows from given query"""
        self._execute(query, args)
        return self.c.fetchall()


if __name__ == 'archivedb.sql':
    log = logging.getLogger(__name__)