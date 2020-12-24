# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/django_s3_storage2/management/commands/s3_sync_meta.py
# Compiled at: 2015-11-24 02:14:29
# Size of source mod 2**32: 914 bytes
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string

class Command(BaseCommand):
    help = 'Syncronizes the meta information on S3 files.'
    args = '[path.to.storage.instance, ...]'

    def handle(self, *storage_paths, **kwargs):
        verbosity = int(kwargs.get('verbosity', 1))
        for storage_path in storage_paths:
            if verbosity >= 1:
                self.stdout.write('Syncing meta for {}'.format(storage_path))
            try:
                storage = import_string(storage_path)
            except ImportError:
                raise CommandError('Could not import {}'.format(storage_path))

            for path in storage.sync_meta_iter():
                if verbosity >= 1:
                    self.stdout.write('  Synced meta for {}'.format(path))
                    continue