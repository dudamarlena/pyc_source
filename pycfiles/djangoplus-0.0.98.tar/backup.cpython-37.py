# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/management/commands/backup.py
# Compiled at: 2018-10-05 12:53:00
# Size of source mod 2**32: 1471 bytes
import os
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        from dropbox import Dropbox
        from dropbox.files import WriteMode
        dropbox_destination = settings.PROJECT_NAME
        client = Dropbox(settings.DROPBOX_TOKEN)
        local_paths = []
        for relative_path in settings.BACKUP_FILES:
            file_or_directory = os.path.join(settings.BASE_DIR, relative_path)
            if os.path.isdir(file_or_directory):
                for root, dirs, files in os.walk(file_or_directory):
                    for filename in files:
                        local_path = os.path.join(root, filename)
                        relative_path = os.path.relpath(local_path, settings.BASE_DIR)
                        dropbox_path = os.path.join(dropbox_destination, relative_path)
                        local_paths.append((local_path, dropbox_path))

            else:
                dropbox_path = os.path.join(dropbox_destination, relative_path)
                local_paths.append((file_or_directory, dropbox_path))

        for local_path, dropbox_path in local_paths:
            dropbox_path = '/{}'.format(dropbox_path)
            print('Uploading {} to {}...'.format(local_path, dropbox_path))
            with open(local_path, 'rb') as (f):
                client.files_upload(f, dropbox_path, WriteMode.overwrite)