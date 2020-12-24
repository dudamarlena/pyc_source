# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/Commands/Init.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 397 bytes
from .Command import Command

class Init(Command):
    command = 'init'
    help = 'Initialize new document repository'

    def set_args(self, subparser):
        subparser.add_argument('--force', help='Overwrite existing document repository', action='store_true')

    def run(self, args):
        from ..Database import Database
        Database.init(dataDir=(args.data_dir), clobber=(args.force))