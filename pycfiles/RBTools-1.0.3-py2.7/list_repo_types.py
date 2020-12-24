# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/list_repo_types.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals
from rbtools.clients import print_clients
from rbtools.commands import Command

class ListRepoTypes(Command):
    """List available repository types."""
    name = b'list-repo-types'
    author = b'The Review Board Project'
    description = b'Print a list of supported repository types.'

    def main(self, *args):
        print_clients(self.config, self.options)