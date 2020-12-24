# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ls_var_spool_clientmq.py
# Compiled at: 2019-05-16 13:41:33
"""
LsVarSpoolClientmq - command ``ls -ln /var/spool/clientmqueue``
===============================================================

The ``ls -ln /var/spool/clientmqueue`` command provides information for the listing of the ``/var/spool/clientmqueue`` directory.

Sample input is shown in the Examples. See ``FileListing`` class for
additional information.

Sample directory list::

    total 40
    -rw-rw---- 1 51 51   4 Jul 11 02:32 dfw6B6Wilr002718
    -rw-rw---- 1 51 51   4 Jul 11 02:32 dfw6B6WixJ002715
    -rw-rw---- 1 51 51   4 Jul 11 02:32 dfw6B6WjP6002721
    -rw-rw---- 1 51 51 817 Jul 11 03:35 dfw6B7Z8BB002906
    -rw-rw---- 1 51 51 817 Jul 11 04:02 dfw6B822T0011150

Examples:

    >>> "dfw6B6Wilr002718" in ls_var_spool_clientmq
    False
    >>> "/var/spool/clientmqueue" in ls_var_spool_clientmq
    True
    >>> ls_var_spool_clientmq.dir_entry('/var/spool/clientmqueue', 'dfw6B6Wilr002718')['type']
    '-'
"""
from insights.specs import Specs
from .. import CommandParser, parser
from .. import FileListing

@parser(Specs.ls_var_spool_clientmq)
class LsVarSpoolClientmq(CommandParser, FileListing):
    """Parses output of ``ls -ln /var/spool/clientmqueue`` command."""
    pass