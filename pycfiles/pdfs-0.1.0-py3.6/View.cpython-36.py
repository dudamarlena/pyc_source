# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/Commands/View.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 868 bytes
from .Command import Command
from .Completers import citekeyCompleter, attachmentCompleter

class View(Command):
    command = 'view'
    help = 'View article PDF and attachements'

    def set_args(self, subparser):
        subparser.add_argument('key', metavar='CITE_KEY', type=str).completer = citekeyCompleter
        subparser.add_argument('label', nargs='?', metavar='NAME', default='PDF', type=str).completer = attachmentCompleter

    def run(self, args):
        import subprocess
        from ..Database import Database
        from ..Exceptions import UserException
        db = Database(dataDir=(args.data_dir))
        try:
            e = next(x for x in db.works if x.key() == args.key)
        except StopIteration:
            raise UserException('Key {} not found'.format(args.key))

        subprocess.Popen(['xdg-open', db.getFile(e, args.label)])