# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /volume/flask_db2/base.py
# Compiled at: 2015-08-13 17:15:33
# Size of source mod 2**32: 3044 bytes
"""
    flaskext.db2
    ~~~~~~~~~~~~~~~~~~~
    An extension to Flask for handling DB2 connections.
    :copyright: (c) 2015 by Justin Wilson <flask-db2@minty.io>.
    :license: BSD, see LICENSE for more details.
"""
import ibm_db, ibm_db_dbi
from flask import current_app
from flask import _app_ctx_stack as stack

class DB2(object):
    __doc__ = 'Manages connections to an IBM DB2 database using the ibm_db_dbi driver.\n    '

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize a :class:`~flask.Flask` application for use with
        this extension.
        """
        app.config.setdefault('DB2_DATABASE', 'sample')
        app.config.setdefault('DB2_HOSTNAME', 'localhost')
        app.config.setdefault('DB2_PORT', 50000)
        app.config.setdefault('DB2_PROTOCOL', 'TCPIP')
        app.config.setdefault('DB2_USER', 'db2inst1')
        app.config.setdefault('DB2_PASSWORD', 'db2inst1')
        app.config.setdefault('DB2_POOL_CONNECTIONS', True)
        app.teardown_appcontext(self.teardown)

    def _connection_string(self, config):
        conn_fmt = 'DATABASE={};HOSTNAME={};PORT={};PROTOCOL={};UID={};PWD={}'
        return conn_fmt.format(config['DB2_DATABASE'], config['DB2_HOSTNAME'], config['DB2_PORT'], config['DB2_PROTOCOL'], config['DB2_USER'], config['DB2_PASSWORD'])

    def connect(self, config=None):
        """Returns a new database connection.

        When `DB2_POOL_CONNECTIONS` is true a connection supporting pooling
        is used.

        :param config: configuration object used to establish connections.
                       current_app.config is used by default.
        """
        if config is None:
            config = current_app.config
        conn_string = self._connection_string(config)
        if config['DB2_POOL_CONNECTIONS']:
            connection = ibm_db.pconnect(conn_string, '', '')
        else:
            connection = ibm_db.connect(conn_string, '', '')
        return ibm_db_dbi.Connection(connection)

    def teardown(self, exception):
        """Closes the database connection.
        """
        ctx = stack.top
        if hasattr(ctx, 'ibm_db'):
            ctx.ibm_db.close()

    @property
    def connection(self):
        """Returns an ibm_db_dbi Connection object.
        """
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'ibm_db'):
                ctx.ibm_db = self.connect()
            return ctx.ibm_db

    def row_factory(self, cursor, row, mapper=None):
        """Returns a dictionary of {COLUMN: VALUE} for the given cursor/row.

        :param cursor: db2 cursor
        :param row: db2 row
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            key = col[0]
            if mapper is not None:
                key = mapper.get(key, key)
            d[key] = row[idx]

        return d