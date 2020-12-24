# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/commands/dump.py
# Compiled at: 2014-06-16 16:12:17
import json
from kolekto.printer import printer
from kolekto.commands import Command

class Dump(Command):
    """ Dump the whole database into json.
    """
    help = 'dump database into json'

    def run(self, args, config):
        mdb = self.get_metadata_db(args.tree)
        dump = [ {'hash': x, 'movie': y} for x, y in mdb.itermovies() ]
        json.dump(dump, printer.output)