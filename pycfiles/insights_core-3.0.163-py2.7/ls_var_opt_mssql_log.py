# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ls_var_opt_mssql_log.py
# Compiled at: 2019-05-16 13:41:33
"""
LsVarOptMssqlLog - command ``ls -la /var/opt/mssql/log``
========================================================

This parser reads the ``/var/opt/mssql/log`` directory listings and uses the
FileListing parser class to provide a common access to them.

"""
from insights import FileListing, parser, CommandParser
from insights.specs import Specs

@parser(Specs.ls_var_opt_mssql_log)
class LsVarOptMssqlLog(CommandParser, FileListing):
    """
    A parser for accessing "ls -la /var/opt/mssql/log".

    Examples:
        >>> '/var/opt/mssql/log' in ls_mssql_log
        True
        >>> ls_mssql_log.dir_contains('/var/opt/mssql/log', 'messages')
        False
    """
    pass