# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ls_var_tmp.py
# Compiled at: 2019-05-16 13:41:33
"""
LsVarTmp - command ``ls -ln /var/tmp``
======================================

The ``ls -ln /var/tmp`` command provides information for the listing of the
``/var/tmp`` directory.

Sample input is shown in the Examples. See ``FileListing`` class for
additional information.

Sample directory list::

    /var/tmp:
    total 20
    drwxr-xr-x.  2 0 0 4096 Mar 26 02:25 a1
    drwxr-xr-x.  2 0 0 4096 Mar 26 02:25 a2
    drwxr-xr-x.  2 0 0 4096 Apr 28  2018 foreman-ssh-cmd-fc3f65c9-2b35-480d-87e3-1d971433d6ad

Examples:

    >>> "a1" in ls_var_tmp
    False
    >>> "/var/tmp" in ls_var_tmp
    True
    >>> ls_var_tmp.dir_entry('/var/tmp', 'a1')['type']
    'd'
"""
from insights.specs import Specs
from insights.core.filters import add_filter
from .. import FileListing
from .. import parser, CommandParser
add_filter(Specs.ls_var_tmp, '/var/tmp')

@parser(Specs.ls_var_tmp)
class LsVarTmp(CommandParser, FileListing):
    """Parses output of ``ls -ln /var/tmp`` command."""
    pass