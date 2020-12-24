# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/commands/gpg/fingerprint.py
# Compiled at: 2015-08-31 08:17:33
from pgp.commands.gpg.list_keys import Command as ListKeysCommand

class Command(ListKeysCommand):

    def __init__(self, *args, **kwargs):
        ListKeysCommand.__init__(self, show_fingerprints=True, *args, **kwargs)