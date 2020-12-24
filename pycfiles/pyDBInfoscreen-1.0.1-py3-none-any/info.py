# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/info.py
# Compiled at: 2013-03-15 20:24:23
import os
from import_relative import import_relative
Mbase_submgr = import_relative('base_submgr', top_name='pydbgr')

class InfoCommand(Mbase_submgr.SubcommandMgr):
    """Generic command for showing things about the program being debugged. 

You can give unique prefix of the name of a subcommand to get
information about just that subcommand.

Type `info` for a list of *info* subcommands and what they do.
Type `help info *` for just a list of *info* subcommands.
"""
    __module__ = __name__
    aliases = ('i', )
    category = 'status'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Information about debugged program and its environment'


if __name__ == '__main__':
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = InfoCommand(cp, 'info')
    command.run(['info'])