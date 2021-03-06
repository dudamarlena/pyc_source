# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ls_var_spool_postfix_maildrop.py
# Compiled at: 2019-05-16 13:41:33
"""
LsVarSpoolPostfixMaildrop - command ``ls -ln /var/spool/postfix/maildrop``
==========================================================================

The ``ls -ln /var/spool/postfix/maildrop`` command provides information for the listing of the ``/var/spool/postfix/maildrop`` directory.

Sample input is shown in the Examples. See ``FileListing`` class for
additional information.

Sample directory list::

    total 20
    -rwxr--r--. 1 0 90 258 Jul 11 15:54 55D6821C286
    -rwxr--r--. 1 0 90 282 Jul 11 15:54 5852121C284
    -rwxr--r--. 1 0 90 258 Jul 11 15:54 9FFEC21C287
    -rwxr--r--. 1 0 90 258 Jul 11 15:54 E9A4521C285
    -rwxr--r--. 1 0 90 258 Jul 11 15:54 EA60F21C288

Examples:

    >>> "55D6821C286" in ls_var_spool_postfix_maildrop
    False
    >>> "/var/spool/postfix/maildrop" in ls_var_spool_postfix_maildrop
    True
    >>> ls_var_spool_postfix_maildrop.dir_entry('/var/spool/postfix/maildrop', '55D6821C286')['type']
    '-'
"""
from insights.specs import Specs
from .. import CommandParser, parser
from .. import FileListing

@parser(Specs.ls_var_spool_postfix_maildrop)
class LsVarSpoolPostfixMaildrop(CommandParser, FileListing):
    """Parses output of ``ls -ln /var/spool/postfix/maildrop`` command."""
    pass