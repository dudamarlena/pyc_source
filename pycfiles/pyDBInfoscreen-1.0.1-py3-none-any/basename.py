# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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