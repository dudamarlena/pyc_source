# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/commands/gpg/multifile.py
# Compiled at: 2015-08-31 08:17:33


class MultifileCommand(object):

    def __init__(self, subcommand):
        self.subcommand = subcommand

    def run(self, *args):
        for arg in self.args:
            self.subcommand.run(arg)