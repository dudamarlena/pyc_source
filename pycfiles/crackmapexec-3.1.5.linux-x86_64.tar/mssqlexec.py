# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/execmethods/mssqlexec.py
# Compiled at: 2016-12-29 01:49:52
import traceback

class MSSQLEXEC:

    def __init__(self, connection):
        self.mssql_conn = connection
        self.outputBuffer = ''

    def execute(self, command, output=False):
        try:
            self.enable_xp_cmdshell()
            self.mssql_conn.sql_query(("exec master..xp_cmdshell '{}'").format(command))
            if output:
                self.mssql_conn.printReplies()
                self.mssql_conn.colMeta[0]['TypeData'] = 160
                self.outputBuffer = self.mssql_conn.printRows()
            self.disable_xp_cmdshell()
            return self.outputBuffer
        except Exception:
            traceback.print_exc()

    def enable_xp_cmdshell(self):
        self.mssql_conn.sql_query("exec master.dbo.sp_configure 'show advanced options',1;RECONFIGURE;exec master.dbo.sp_configure 'xp_cmdshell', 1;RECONFIGURE;")

    def disable_xp_cmdshell(self):
        self.mssql_conn.sql_query("exec sp_configure 'xp_cmdshell', 0 ;RECONFIGURE;exec sp_configure 'show advanced options', 0 ;RECONFIGURE;")