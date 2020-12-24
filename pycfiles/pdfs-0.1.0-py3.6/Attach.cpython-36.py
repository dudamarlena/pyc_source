# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/Commands/Attach.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 963 bytes
from .Command import Command
from .Completers import citekeyCompleter
from argcomplete.completers import FilesCompleter

class Attach(Command):
    command = 'attach'
    help = 'Attach a supplementary file'

    def set_args(self, subparser):
        subparser.add_argument('key', metavar='CITE_KEY', type=str).completer = citekeyCompleter
        subparser.add_argument('file', metavar='ATTACHMENT', type=str).completer = FilesCompleter(directories=False)
        subparser.add_argument('--name', '-n', metavar='NAME', type=str)

    def run(self, args):
        from ..Database import Database
        from ..Exceptions import UserException
        db = Database(dataDir=(args.data_dir))
        try:
            e = next(x for x in db.works if x.key() == args.key)
        except StopIteration:
            raise UserException('Key {} not found'.format(args.key))

        e.tags = sorted((set(e.tags) | set(args.add)) - set(args.remove))
        db.save()