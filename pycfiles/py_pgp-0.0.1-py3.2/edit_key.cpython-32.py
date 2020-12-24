# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/commands/gpg/edit_key.py
# Compiled at: 2015-08-31 08:17:33
from .list_ import ListCommand

class Command(ListCommand):

    def __init__(self, list_options, default_prefs_list):
        ListCommand.__init__(self, list_options)
        self.default_prefs_list = default_prefs_list