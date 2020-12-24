# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/basename.py
# Compiled at: 2013-03-18 05:57:53
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')

class ShowBasename(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """**show basename**

Show whether filenames are reported with just the basename or the
fully qualified filename.

Change with **set basename**
"""
    __module__ = __name__
    short_help = 'Show the basename portion only of filenames'
    min_abbrev = len('ba')


if __name__ == '__main__':
    Mhelper = import_relative('__demo_helper__', '.', 'pydbgr')
    Mhelper.demo_run(ShowBasename)