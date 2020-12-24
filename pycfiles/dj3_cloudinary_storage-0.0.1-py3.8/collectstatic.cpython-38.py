# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cloudinary_storage/management/commands/collectstatic.py
# Compiled at: 2020-03-05 09:54:42
# Size of source mod 2**32: 1419 bytes
from django.contrib.staticfiles.management.commands import collectstatic
from django.conf import settings

class Command(collectstatic.Command):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--upload-unhashed-files', action='store_true', dest='upload_unhashed_files', help='Apart from hashed files, upload unhashed ones as well. Use only when you need it.')

    def set_options(self, **options):
        (super(Command, self).set_options)(**options)
        self.upload_unhashed_files = options['upload_unhashed_files']

    def delete_file(self, path, prefixed_path, source_storage):
        """
        Overwritten to prevent any deletion during command execution.
        Unnecessary static files can be deleted with 'deleteredundantstatic' command.
        """
        return True

    def copy_file(self, path, prefixed_path, source_storage):
        if settings.STATICFILES_STORAGE == 'cloudinary_storage.storage.StaticCloudinaryStorage' or self.upload_unhashed_files:
            super(Command, self).copy_file(path, prefixed_path, source_storage)