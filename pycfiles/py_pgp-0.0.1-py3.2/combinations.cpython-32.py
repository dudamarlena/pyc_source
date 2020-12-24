# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/commands/gpg/combinations.py
# Compiled at: 2015-08-31 08:17:33
from pgp.commands.gpg.check_sigs import Command as CheckSigsCommand
from pgp.commands.gpg.list_sigs import Command as ListSigsCommand

class EncryptSymmetricAndSign(object):
    multifile = True

    def __init__(self):
        pass

    def run(self, *args):
        pass


class EncryptAndSign(object):
    multifile = True

    def __init__(self):
        pass

    def run(self, *args):
        pass


class SymmetricAndSign(object):

    def __init__(self):
        pass

    def run(self, *args):
        pass


class FingerprintCheckSigs(CheckSigsCommand):

    def __init__(self, show_fingerprints, *args, **kwargs):
        CheckSigsCommand.__init__(self, show_fingerprints=1, *args, **kwargs)


class FingerprintListSigs(ListSigsCommand):

    def __init__(self, show_fingerprints, *args, **kwargs):
        CheckSigsCommand.__init__(self, show_fingerprints=show_fingerprints, *args, **kwargs)