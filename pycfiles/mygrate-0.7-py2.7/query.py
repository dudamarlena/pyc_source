# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mygrate/query.py
# Compiled at: 2014-07-18 08:16:56
import os, os.path, sys, logging, optparse, cPickle, MySQLdb, MySQLdb.cursors

class InitialQuery(object):
    """Manages direct queries to MySQL for importing, validation, and
    re-validation.

    """

    def __init__(self, mysql_info, callbacks, action='INSERT', streaming=False):
        self.mysql_info = mysql_info
        self.callbacks = callbacks
        self.action = action
        self.streaming = streaming
        self.log = logging.getLogger('mygrate.query')

    def run_callback(self, table, cols):
        """Executes the INSERT callback for the given table.

        :param table: The table being imported from.
        :param cols: The column dict containing the row data.

        """
        self.callbacks.execute(table, self.action, cols)

    def get_connection(self, db):
        """Creates and returns a connection to the MySQL server and selects the
        given database.

        :param db: The database name to select after connection.
        :returns: A MySQL connection object.

        """
        kwargs = self.mysql_info.copy()
        kwargs['db'] = db
        kwargs['charset'] = 'utf8'
        if self.streaming:
            kwargs['cursorclass'] = MySQLdb.cursors.SSDictCursor
        else:
            kwargs['cursorclass'] = MySQLdb.cursors.DictCursor
        conn = MySQLdb.connect(**kwargs)
        return conn

    def process_table(self, full_table):
        """Runs SELECT queries against the table until the entire table
        contents have been processed. Rows are then passed to `run_callback()`.

        The table should not be receiving updates during the execution of this
        method. Any modifications to the table may disrupt the process and
        result in lost or duplicate data.

        :param full_table: The database and table names, separated by a period,
                           as given on the command line.

        """
        db, table = full_table.split('.')
        conn = self.get_connection(db)
        cur = conn.cursor()
        try:
            try:
                sql = ('SELECT * FROM `{0}`').format(table)
                cur.execute(sql)
                for row in cur:
                    self.run_callback(full_table, row)

            except Exception:
                self.log.exception('Unhandled exception')

        finally:
            cur.close()
            conn.close()


def main():
    description = 'This program attempts to import an entire table by creating job tasks for each\nrow.\n\nConfiguration for %prog is done with configuration files. This is either\n/etc/mygrate.conf, ~/.mygrate.conf, or an alternative specified by the\nMYGRATE_CONFIG environment variable.\n\nIf no tables are given in the command-line arguments, all tables that have\nregistered callbacks are queried.\n'
    usage = 'usage: %prog [options] [<database>.<table> ...]'
    op = optparse.OptionParser(usage=usage, description=description)
    op.add_option('-s', '--stream', action='store_true', default=False, help='Stream the query results from the MySQL server.')
    options, requested_tables = op.parse_args()
    from .config import cfg
    from .callbacks import MygrateCallbacks
    callbacks = MygrateCallbacks()
    mysql_info = cfg.get_mysql_connection_info()
    cfg.call_entry_point(callbacks)
    if not requested_tables:
        requested_tables = callbacks.get_registered_tables()
    query = InitialQuery(mysql_info, callbacks, streaming=options.stream)
    for table in requested_tables:
        query.process_table(table)


if __name__ == '__main__':
    main()