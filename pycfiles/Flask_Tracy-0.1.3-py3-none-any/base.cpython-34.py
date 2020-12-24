# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /volume/flask_dms_db2/base.py
# Compiled at: 2015-08-13 11:24:27
# Size of source mod 2**32: 1407 bytes
"""
    flaskext.dms_db2
    ~~~~~~~~~~~~~~~~~~~
    An extension to Flask for handling DB2 connections.
"""
from flask import current_app
from flask_db2 import DB2
from flask_dms_db2.servers import servers
sql_enterprise_server = '\nSELECT\n    DTDMS_SERVER_ID\nFROM\n    EISFUSION.DT_DEALERMASTER\nWHERE\n    ENTERPRISECODEDMS = ?\n    FETCH FIRST 1 ROWS ONLY\n'

class DMS_DB2(DB2):
    __doc__ = 'Subset of `flask_db2.DB2` that adds support for getting\n    enterprise connections.\n    '

    def server_name(self, enterprise_code):
        """Returns the server name for the given enterprise code.

        :param enterprise_code: enterprise code to pull the server name for.
        """
        cursor = self.connection.cursor()
        cursor.execute(sql_enterprise_server, (enterprise_code,))
        row = cursor.fetchone()
        return row[0]

    def enterprise_connection(self, enterprise_code):
        """Returns a connection for the given enterprise code.

        :param enterprise_code: enterprise code to pull the server name for.
        """
        server_name = self.server_name(enterprise_code)
        server = servers.get(server_name)
        if server is None:
            return self.connection
        config = dict(current_app.config)
        config['DB2_HOSTNAME'] = server['hostname']
        config['DB2_DATABASE'] = server['database']
        return self.connect(config=config)