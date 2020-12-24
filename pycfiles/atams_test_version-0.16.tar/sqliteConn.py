# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIGPC4\Desktop\atamsPackage\build\lib\atams\sqliteConn.py
# Compiled at: 2018-09-27 01:44:22
import sqlite3
from sqlite3 import Error

class SQLite:

    def __init__(self):
        self.status = ''
        self.conn = None
        return

    def create_connection(self, dbname):
        print dbname
        try:
            self.conn = sqlite3.connect(dbname, check_same_thread=False)
            return self.conn
        except Error as e:
            print (
             'db connection error', e)
            self.status = e
            return

        return

    def create_table(self, conn, TABLE_DEF):
        try:
            self.conn.execute(TABLE_DEF)
            return True
        except Error as e:
            print e
            self.status = e
            return

        return

    def clear_table(self, conn, DELETE_DEF):
        try:
            self.conn.execute(DELETE_DEF)
            return True
        except Error as e:
            print e
            self.status = e
            return

        return

    def sqlite3_backup(dbfile, backupdir):
        """Create timestamped database copy"""
        if not os.path.isdir(backupdir):
            raise Exception(('Backup directory does not exist: {}').format(backupdir))
        backup_file = os.path.join(backupdir, os.path.basename(dbfile) + time.strftime('-%Y%m%d-%H%M%S'))
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()
        cursor.execute('begin immediate')
        shutil.copyfile(dbfile, backup_file)
        print ('\nCreating {}...').format(backup_file)
        connection.rollback()

    def clean_data(backup_dir):
        """Delete files older than NO_OF_DAYS days"""
        print '\n------------------------------'
        print 'Cleaning up old backups'
        for filename in os.listdir(backup_dir):
            backup_file = os.path.join(backup_dir, filename)
            if os.stat(backup_file).st_ctime < time.time() - NO_OF_DAYS * 86400:
                if os.path.isfile(backup_file):
                    os.remove(backup_file)
                    print ('Deleting {}...').format(ibackup_file)