# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ls_usr_sbin.py
# Compiled at: 2019-05-16 13:41:33
"""
LsUsrSbin - command ``ls -ln /usr/sbin``
========================================

The ``ls -ln /usr/sbin`` command provides information for the listing of the
``/usr/sbin`` directory.

Sample input is shown in the Examples. See ``FileListing`` class for
additional information.

For ls_usr_sbin, it may collect a lot of files or directories that may not be
necessary, so a default filter `add_filter(Specs.ls_usr_sbin, "total")` has
been added in this parser.

If addtional file or directory need to be collected by this parser, please
add related filter to corresponding code.

Sample added filter:

    >>> add_filter(Specs.ls_usr_sbin, "accessdb")

Sample directory list collected::

    total 41472
    -rwxr-xr-x. 1 0  0   11720 Mar 18  2014 accessdb

Examples:

    >>> "accessdb" in ls_usr_sbin
    False
    >>> "/usr/sbin" in ls_usr_sbin
    True
    >>> ls_usr_sbin.dir_entry('/usr/sbin', 'accessdb')['type']
    '-'

Sample added filter:

    >>> add_filter(Specs.ls_usr_sbin, "accessdb")
    >>> add_filter(Specs.ls_usr_sbin, "postdrop")

Sample directory list collected::

    total 41472
    -rwxr-xr-x. 1 0  0   11720 Mar 18  2014 accessdb
    -rwxr-sr-x. 1 0 90  218552 Jan 27  2014 postdrop

Examples:

    >>> "accessdb" in ls_usr_sbin
    False
    >>> "/usr/sbin" in ls_usr_sbin
    True
    >>> ls_usr_sbin.dir_entry('/usr/sbin', 'accessdb')['type']
    '-'
    >>> ls_usr_sbin.dir_entry('/usr/sbin', 'postdrop')['type']
    '-'
"""
from insights.core.filters import add_filter
from insights.specs import Specs
from .. import CommandParser, parser
from .. import FileListing
add_filter(Specs.ls_usr_sbin, 'total')

@parser(Specs.ls_usr_sbin)
class LsUsrSbin(CommandParser, FileListing):
    """Parses output of ``ls -ln /usr/sbin`` command."""
    pass