# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/script/shell.py
# Compiled at: 2007-03-21 14:34:41
"""Python shell command.

For copyright, license, and warranty, see bottom of file.
"""
import sys, schevo.database
from schevo.script.command import Command
from schevo.script import opt
usage = "schevo shell [options] DBFILE\n\nDBFILE: The database file to open.  The database will be present as\nthe 'db' variable in the shell.\n\nIf IPython is available, it will be used automatically."

def _parser():
    p = opt.parser(usage)
    return p


class Shell(Command):
    __module__ = __name__
    name = 'Python Shell'
    description = 'Start a Python shell with an open database.'

    def main(self, arg0, args):
        print
        print
        parser = _parser()
        (options, args) = parser.parse_args(list(args))
        if len(args) != 1:
            print 'DBFILE must be specified.'
            return 1
        db_filename = args[0]
        print 'Opened database', db_filename
        db = schevo.database.open(db_filename)
        locals = dict(__name__='schevo-shell', db=db)
        old_argv = sys.argv
        sys.argv = sys.argv[0:1]
        try:
            try:
                import IPython
            except ImportError:
                import code
                code.interact(local=locals)
            else:
                shell = IPython.Shell.IPShell(user_ns=locals)
                shell.mainloop()

        finally:
            sys.argv = old_argv


start = Shell