# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/staticfiles/management/commands/collectstatic.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import os, sys
from optparse import make_option
from django.core.files.storage import FileSystemStorage
from django.core.management.base import CommandError, NoArgsCommand
from django.utils.encoding import smart_text
from django.utils.datastructures import SortedDict
from django.utils.six.moves import input
from django.contrib.staticfiles import finders, storage

class Command(NoArgsCommand):
    """
    Command that allows to copy or symlink static files from different
    locations to the settings.STATIC_ROOT.
    """
    option_list = NoArgsCommand.option_list + (
     make_option(b'--noinput', action=b'store_false', dest=b'interactive', default=True, help=b'Do NOT prompt the user for input of any kind.'),
     make_option(b'--no-post-process', action=b'store_false', dest=b'post_process', default=True, help=b'Do NOT post process collected files.'),
     make_option(b'-i', b'--ignore', action=b'append', default=[], dest=b'ignore_patterns', metavar=b'PATTERN', help=b'Ignore files or directories matching this glob-style pattern. Use multiple times to ignore more.'),
     make_option(b'-n', b'--dry-run', action=b'store_true', dest=b'dry_run', default=False, help=b'Do everything except modify the filesystem.'),
     make_option(b'-c', b'--clear', action=b'store_true', dest=b'clear', default=False, help=b'Clear the existing files using the storage before trying to copy or link the original file.'),
     make_option(b'-l', b'--link', action=b'store_true', dest=b'link', default=False, help=b'Create a symbolic link to each file instead of copying.'),
     make_option(b'--no-default-ignore', action=b'store_false', dest=b'use_default_ignore_patterns', default=True, help=b"Don't ignore the common private glob-style patterns 'CVS', '.*' and '*~'."))
    help = b'Collect static files in a single location.'
    requires_model_validation = False

    def __init__(self, *args, **kwargs):
        super(NoArgsCommand, self).__init__(*args, **kwargs)
        self.copied_files = []
        self.symlinked_files = []
        self.unmodified_files = []
        self.post_processed_files = []
        self.storage = storage.staticfiles_storage
        try:
            self.storage.path(b'')
        except NotImplementedError:
            self.local = False
        else:
            self.local = True

        if hasattr(os, b'stat_float_times'):
            os.stat_float_times(False)

    def set_options(self, **options):
        """
        Set instance variables based on an options dict
        """
        self.interactive = options[b'interactive']
        self.verbosity = int(options.get(b'verbosity', 1))
        self.symlink = options[b'link']
        self.clear = options[b'clear']
        self.dry_run = options[b'dry_run']
        ignore_patterns = options[b'ignore_patterns']
        if options[b'use_default_ignore_patterns']:
            ignore_patterns += [b'CVS', b'.*', b'*~']
        self.ignore_patterns = list(set(ignore_patterns))
        self.post_process = options[b'post_process']

    def collect(self):
        """
        Perform the bulk of the work of collectstatic.

        Split off from handle_noargs() to facilitate testing.
        """
        if self.symlink:
            if sys.platform == b'win32':
                raise CommandError(b'Symlinking is not supported by this platform (%s).' % sys.platform)
            if not self.local:
                raise CommandError(b"Can't symlink to a remote destination.")
        if self.clear:
            self.clear_dir(b'')
        if self.symlink:
            handler = self.link_file
        else:
            handler = self.copy_file
        found_files = SortedDict()
        for finder in finders.get_finders():
            for path, storage in finder.list(self.ignore_patterns):
                if getattr(storage, b'prefix', None):
                    prefixed_path = os.path.join(storage.prefix, path)
                else:
                    prefixed_path = path
                if prefixed_path not in found_files:
                    found_files[prefixed_path] = (
                     storage, path)
                    handler(path, prefixed_path, storage)

        if self.post_process and hasattr(self.storage, b'post_process'):
            processor = self.storage.post_process(found_files, dry_run=self.dry_run)
            for original_path, processed_path, processed in processor:
                if processed:
                    self.log(b"Post-processed '%s' as '%s" % (
                     original_path, processed_path), level=1)
                    self.post_processed_files.append(original_path)
                else:
                    self.log(b"Skipped post-processing '%s'" % original_path)

        return {b'modified': self.copied_files + self.symlinked_files, 
           b'unmodified': self.unmodified_files, 
           b'post_processed': self.post_processed_files}

    def handle_noargs(self, **options):
        self.set_options(**options)
        if isinstance(self.storage, FileSystemStorage) and self.storage.location:
            destination_path = self.storage.location
            destination_display = b':\n\n    %s' % destination_path
        else:
            destination_path = None
            destination_display = b'.'
        if self.clear:
            clear_display = b'This will DELETE EXISTING FILES!'
        else:
            clear_display = b'This will overwrite existing files!'
        if self.interactive:
            confirm = input(b"\nYou have requested to collect static files at the destination\nlocation as specified in your settings%s\n\n%s\nAre you sure you want to do this?\n\nType 'yes' to continue, or 'no' to cancel: " % (
             destination_display, clear_display))
            if confirm != b'yes':
                raise CommandError(b'Collecting static files cancelled.')
        collected = self.collect()
        modified_count = len(collected[b'modified'])
        unmodified_count = len(collected[b'unmodified'])
        post_processed_count = len(collected[b'post_processed'])
        if self.verbosity >= 1:
            template = b'\n%(modified_count)s %(identifier)s %(action)s%(destination)s%(unmodified)s%(post_processed)s.\n'
            summary = template % {b'modified_count': modified_count, 
               b'identifier': b'static file' + (modified_count != 1 and b's' or b''), 
               b'action': self.symlink and b'symlinked' or b'copied', 
               b'destination': destination_path and b" to '%s'" % destination_path or b'', 
               b'unmodified': collected[b'unmodified'] and b', %s unmodified' % unmodified_count or b'', 
               b'post_processed': collected[b'post_processed'] and b', %s post-processed' % post_processed_count or b''}
            self.stdout.write(summary)
        return

    def log(self, msg, level=2):
        """
        Small log helper
        """
        if self.verbosity >= level:
            self.stdout.write(msg)

    def clear_dir(self, path):
        """
        Deletes the given relative path using the destination storage backend.
        """
        dirs, files = self.storage.listdir(path)
        for f in files:
            fpath = os.path.join(path, f)
            if self.dry_run:
                self.log(b"Pretending to delete '%s'" % smart_text(fpath), level=1)
            else:
                self.log(b"Deleting '%s'" % smart_text(fpath), level=1)
                self.storage.delete(fpath)

        for d in dirs:
            self.clear_dir(os.path.join(path, d))

    def delete_file(self, path, prefixed_path, source_storage):
        """
        Checks if the target file should be deleted if it already exists
        """
        if self.storage.exists(prefixed_path):
            try:
                target_last_modified = self.storage.modified_time(prefixed_path)
            except (OSError, NotImplementedError, AttributeError):
                pass

            try:
                source_last_modified = source_storage.modified_time(path)
            except (OSError, NotImplementedError, AttributeError):
                pass

            if self.local:
                full_path = self.storage.path(prefixed_path)
            else:
                full_path = None
            if target_last_modified >= source_last_modified:
                if not (self.symlink and full_path and not os.path.islink(full_path) or not self.symlink and full_path and os.path.islink(full_path)):
                    if prefixed_path not in self.unmodified_files:
                        self.unmodified_files.append(prefixed_path)
                    self.log(b"Skipping '%s' (not modified)" % path)
                    return False
            if self.dry_run:
                self.log(b"Pretending to delete '%s'" % path)
            else:
                self.log(b"Deleting '%s'" % path)
                self.storage.delete(prefixed_path)
        return True

    def link_file(self, path, prefixed_path, source_storage):
        """
        Attempt to link ``path``
        """
        if prefixed_path in self.symlinked_files:
            return self.log(b"Skipping '%s' (already linked earlier)" % path)
        if not self.delete_file(path, prefixed_path, source_storage):
            return
        source_path = source_storage.path(path)
        if self.dry_run:
            self.log(b"Pretending to link '%s'" % source_path, level=1)
        else:
            self.log(b"Linking '%s'" % source_path, level=1)
            full_path = self.storage.path(prefixed_path)
            try:
                os.makedirs(os.path.dirname(full_path))
            except OSError:
                pass

            os.symlink(source_path, full_path)
        if prefixed_path not in self.symlinked_files:
            self.symlinked_files.append(prefixed_path)

    def copy_file(self, path, prefixed_path, source_storage):
        """
        Attempt to copy ``path`` with storage
        """
        if prefixed_path in self.copied_files:
            return self.log(b"Skipping '%s' (already copied earlier)" % path)
        if not self.delete_file(path, prefixed_path, source_storage):
            return
        source_path = source_storage.path(path)
        if self.dry_run:
            self.log(b"Pretending to copy '%s'" % source_path, level=1)
        else:
            self.log(b"Copying '%s'" % source_path, level=1)
            if self.local:
                full_path = self.storage.path(prefixed_path)
                try:
                    os.makedirs(os.path.dirname(full_path))
                except OSError:
                    pass

            with source_storage.open(path) as (source_file):
                self.storage.save(prefixed_path, source_file)
        if prefixed_path not in self.copied_files:
            self.copied_files.append(prefixed_path)