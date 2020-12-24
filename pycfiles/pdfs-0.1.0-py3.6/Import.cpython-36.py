# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/Commands/Import.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 792 bytes
from .Command import Command
from argcomplete.completers import FilesCompleter
from .Completers import citekeyCompleter

class Import(Command):
    command = 'import'
    help = 'Import entries from other database'

    def set_args(self, subparser):
        subparser.add_argument('src', metavar='SRC_REPO', type=str, help='Path to "articles" directory').completer = FilesCompleter
        subparser.add_argument('keys', help='Keys to import', nargs='+', type=str).completer = citekeyCompleter

    def run(self, args):
        from ..Database import Database
        from ..AnsiBib import printWork
        dbDest = Database(dataDir=(args.data_dir))
        dbSrc = Database(dataDir=(args.src))
        for k in args.keys:
            e = dbDest.copyFromDb(dbSrc, k)
            printWork(e)