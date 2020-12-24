# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/management/commands/import-ssh-keys.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.core.management.base import NoArgsCommand
from rbpowerpack.sshdb.importer import import_sshdb_keys

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        import_sshdb_keys()