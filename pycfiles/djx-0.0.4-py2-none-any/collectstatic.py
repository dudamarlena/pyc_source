# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/staticfiles/management/commands/collectstatic.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import os
from collections import OrderedDict
from django.apps import apps
from django.contrib.staticfiles.finders import get_finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.six.moves import input

class Command(BaseCommand):
    """
    Command that allows to copy or symlink static files from different
    locations to the settings.STATIC_ROOT.
    """
    help = b'Collect static files in a single location.'
    requires_system_checks = False

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.copied_files = []
        self.symlinked_files = []
        self.unmodified_files = []
        self.post_processed_files = []
        self.storage = staticfiles_storage
        self.style = no_style()

    @cached_property
    def local(self):
        try:
            self.storage.path(b'')
        except NotImplementedError:
            return False

        return True

    def add_arguments(self, parser):
        parser.add_argument(b'--noinput', b'--no-input', action=b'store_false', dest=b'interactive', default=True, help=b'Do NOT prompt the user for input of any kind.')
        parser.add_argument(b'--no-post-process', action=b'store_false', dest=b'post_process', default=True, help=b'Do NOT post process collected files.')
        parser.add_argument(b'-i', b'--ignore', action=b'append', default=[], dest=b'ignore_patterns', metavar=b'PATTERN', help=b'Ignore files or directories matching this glob-style pattern. Use multiple times to ignore more.')
        parser.add_argument(b'-n', b'--dry-run', action=b'store_true', dest=b'dry_run', default=False, help=b'Do everything except modify the filesystem.')
        parser.add_argument(b'-c', b'--clear', action=b'store_true', dest=b'clear', default=False, help=b'Clear the existing files using the storage before trying to copy or link the original file.')
        parser.add_argument(b'-l', b'--link', action=b'store_true', dest=b'link', default=False, help=b'Create a symbolic link to each file instead of copying.')
        parser.add_argument(b'--no-default-ignore', action=b'store_false', dest=b'use_default_ignore_patterns', default=True, help=b"Don't ignore the common private glob-style patterns (defaults to 'CVS', '.*' and '*~').")

    def set_options(self, **options):
        """
        Set instance variables based on an options dict
        """
        self.interactive = options[b'interactive']
        self.verbosity = options[b'verbosity']
        self.symlink = options[b'link']
        self.clear = options[b'clear']
        self.dry_run = options[b'dry_run']
        ignore_patterns = options[b'ignore_patterns']
        if options[b'use_default_ignore_patterns']:
            ignore_patterns += apps.get_app_config(b'staticfiles').ignore_patterns
        self.ignore_patterns = list(set(ignore_patterns))
        self.post_process = options[b'post_process']

    def collect(self):
        """
        Perform the bulk of the work of collectstatic.

        Split off from handle() to facilitate testing.
        """
        if self.symlink and not self.local:
            raise CommandError(b"Can't symlink to a remote destination.")
        if self.clear:
            self.clear_dir(b'')
        if self.symlink:
            handler = self.link_file
        else:
            handler = self.copy_file
        found_files = OrderedDict()
        for finder in get_finders():
            for path, storage in finder.list(self.ignore_patterns):
                if getattr(storage, b'prefix', None):
                    prefixed_path = os.path.join(storage.prefix, path)
                else:
                    prefixed_path = path
                if prefixed_path not in found_files:
                    found_files[prefixed_path] = (
                     storage, path)
                    handler(path, prefixed_path, storage)
                else:
                    self.log(b"Found another file with the destination path '%s'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path." % prefixed_path, level=1)

        if self.post_process and hasattr(self.storage, b'post_process'):
            processor = self.storage.post_process(found_files, dry_run=self.dry_run)
            for original_path, processed_path, processed in processor:
                if isinstance(processed, Exception):
                    self.stderr.write(b"Post-processing '%s' failed!" % original_path)
                    self.stderr.write(b'')
                    raise processed
                if processed:
                    self.log(b"Post-processed '%s' as '%s'" % (
                     original_path, processed_path), level=1)
                    self.post_processed_files.append(original_path)
                else:
                    self.log(b"Skipped post-processing '%s'" % original_path)

        return {b'modified': self.copied_files + self.symlinked_files, 
           b'unmodified': self.unmodified_files, 
           b'post_processed': self.post_processed_files}

    def handle(self, **options):
        self.set_options(**options)
        message = [
         b'\n']
        if self.dry_run:
            message.append(b'You have activated the --dry-run option so no files will be modified.\n\n')
        message.append(b'You have requested to collect static files at the destination\nlocation as specified in your settings')
        if self.is_local_storage() and self.storage.location:
            destination_path = self.storage.location
            message.append(b':\n\n    %s\n\n' % destination_path)
            should_warn_user = self.storage.exists(destination_path) and any(self.storage.listdir(destination_path))
        else:
            destination_path = None
            message.append(b'.\n\n')
            should_warn_user = True
        if self.interactive and should_warn_user:
            if self.clear:
                message.append(b'This will DELETE ALL FILES in this location!\n')
            else:
                message.append(b'This will overwrite existing files!\n')
            message.append(b"Are you sure you want to do this?\n\nType 'yes' to continue, or 'no' to cancel: ")
            if input((b'').join(message)) != b'yes':
                raise CommandError(b'Collecting static files cancelled.')
        collected = self.collect()
        modified_count = len(collected[b'modified'])
        unmodified_count = len(collected[b'unmodified'])
        post_processed_count = len(collected[b'post_processed'])
        if self.verbosity >= 1:
            template = b'\n%(modified_count)s %(identifier)s %(action)s%(destination)s%(unmodified)s%(post_processed)s.\n'
            summary = template % {b'modified_count': modified_count, 
               b'identifier': b'static file' + (b'' if modified_count == 1 else b's'), 
               b'action': b'symlinked' if self.symlink else b'copied', 
               b'destination': b" to '%s'" % destination_path if destination_path else b'', 
               b'unmodified': b', %s unmodified' % unmodified_count if collected[b'unmodified'] else b'', 
               b'post_processed': collected[b'post_processed'] and b', %s post-processed' % post_processed_count or b''}
            return summary
        else:
            return

    def log(self, msg, level=2):
        """
        Small log helper
        """
        if self.verbosity >= level:
            self.stdout.write(msg)

    def is_local_storage(self):
        return isinstance(self.storage, FileSystemStorage)

    def clear_dir(self, path):
        """
        Deletes the given relative path using the destination storage backend.
        """
        if not self.storage.exists(path):
            return
        dirs, files = self.storage.listdir(path)
        for f in files:
            fpath = os.path.join(path, f)
            if self.dry_run:
                self.log(b"Pretending to delete '%s'" % force_text(fpath), level=1)
            else:
                self.log(b"Deleting '%s'" % force_text(fpath), level=1)
                try:
                    full_path = self.storage.path(fpath)
                except NotImplementedError:
                    self.storage.delete(fpath)
                else:
                    if not os.path.exists(full_path) and os.path.lexists(full_path):
                        os.unlink(full_path)
                    else:
                        self.storage.delete(fpath)

        for d in dirs:
            self.clear_dir(os.path.join(path, d))

    def delete_file(self, path, prefixed_path, source_storage):
        """
        Checks if the target file should be deleted if it already exists
        """
        if self.storage.exists(prefixed_path):
            try:
                target_last_modified = self.storage.get_modified_time(prefixed_path)
            except (OSError, NotImplementedError, AttributeError):
                pass
            else:
                try:
                    source_last_modified = source_storage.get_modified_time(path)
                except (OSError, NotImplementedError, AttributeError):
                    pass
                else:
                    if self.local:
                        full_path = self.storage.path(prefixed_path)
                        can_skip_unmodified_files = not self.symlink ^ os.path.islink(full_path)
                    else:
                        full_path = None
                        can_skip_unmodified_files = True
                    file_is_unmodified = target_last_modified.replace(microsecond=0) >= source_last_modified.replace(microsecond=0)
                    if file_is_unmodified and can_skip_unmodified_files:
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

            try:
                if os.path.lexists(full_path):
                    os.unlink(full_path)
                os.symlink(source_path, full_path)
            except AttributeError:
                import platform
                raise CommandError(b'Symlinking is not supported by Python %s.' % platform.python_version())
            except NotImplementedError:
                import platform
                raise CommandError(b'Symlinking is not supported in this platform (%s).' % platform.platform())
            except OSError as e:
                raise CommandError(e)

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
            with source_storage.open(path) as (source_file):
                self.storage.save(prefixed_path, source_file)
        self.copied_files.append(prefixed_path)