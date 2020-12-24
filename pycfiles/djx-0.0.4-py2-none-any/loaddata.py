# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/loaddata.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import glob, gzip, os, warnings, zipfile
from itertools import product
from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.core.management.utils import parse_apps_and_model_labels
from django.db import DEFAULT_DB_ALIAS, DatabaseError, IntegrityError, connections, router, transaction
from django.utils import lru_cache
from django.utils._os import upath
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.glob import glob_escape
try:
    import bz2
    has_bz2 = True
except ImportError:
    has_bz2 = False

class Command(BaseCommand):
    help = b'Installs the named fixture(s) in the database.'
    missing_args_message = b'No database fixture specified. Please provide the path of at least one fixture in the command line.'

    def add_arguments(self, parser):
        parser.add_argument(b'args', metavar=b'fixture', nargs=b'+', help=b'Fixture labels.')
        parser.add_argument(b'--database', action=b'store', dest=b'database', default=DEFAULT_DB_ALIAS, help=b'Nominates a specific database to load fixtures into. Defaults to the "default" database.')
        parser.add_argument(b'--app', action=b'store', dest=b'app_label', default=None, help=b'Only look for fixtures in the specified app.')
        parser.add_argument(b'--ignorenonexistent', b'-i', action=b'store_true', dest=b'ignore', default=False, help=b'Ignores entries in the serialized data for fields that do not currently exist on the model.')
        parser.add_argument(b'-e', b'--exclude', dest=b'exclude', action=b'append', default=[], help=b'An app_label or app_label.ModelName to exclude. Can be used multiple times.')
        return

    def handle(self, *fixture_labels, **options):
        self.ignore = options[b'ignore']
        self.using = options[b'database']
        self.app_label = options[b'app_label']
        self.verbosity = options[b'verbosity']
        self.excluded_models, self.excluded_apps = parse_apps_and_model_labels(options[b'exclude'])
        with transaction.atomic(using=self.using):
            self.loaddata(fixture_labels)
        if transaction.get_autocommit(self.using):
            connections[self.using].close()

    def loaddata(self, fixture_labels):
        connection = connections[self.using]
        self.fixture_count = 0
        self.loaded_object_count = 0
        self.fixture_object_count = 0
        self.models = set()
        self.serialization_formats = serializers.get_public_serializer_formats()
        self.compression_formats = {None: (
                open, b'rb'), 
           b'gz': (
                 gzip.GzipFile, b'rb'), 
           b'zip': (
                  SingleZipReader, b'r')}
        if has_bz2:
            self.compression_formats[b'bz2'] = (
             bz2.BZ2File, b'r')
        for fixture_label in fixture_labels:
            if self.find_fixtures(fixture_label):
                break
        else:
            return

        with connection.constraint_checks_disabled():
            for fixture_label in fixture_labels:
                self.load_label(fixture_label)

        table_names = [ model._meta.db_table for model in self.models ]
        try:
            connection.check_constraints(table_names=table_names)
        except Exception as e:
            e.args = (
             b'Problem installing fixtures: %s' % e,)
            raise

        if self.loaded_object_count > 0:
            sequence_sql = connection.ops.sequence_reset_sql(no_style(), self.models)
            if sequence_sql:
                if self.verbosity >= 2:
                    self.stdout.write(b'Resetting sequences\n')
                with connection.cursor() as (cursor):
                    for line in sequence_sql:
                        cursor.execute(line)

        if self.verbosity >= 1:
            if self.fixture_object_count == self.loaded_object_count:
                self.stdout.write(b'Installed %d object(s) from %d fixture(s)' % (
                 self.loaded_object_count, self.fixture_count))
            else:
                self.stdout.write(b'Installed %d object(s) (of %d) from %d fixture(s)' % (
                 self.loaded_object_count, self.fixture_object_count, self.fixture_count))
        return

    def load_label(self, fixture_label):
        """
        Loads fixtures files for a given label.
        """
        show_progress = self.verbosity >= 3
        for fixture_file, fixture_dir, fixture_name in self.find_fixtures(fixture_label):
            _, ser_fmt, cmp_fmt = self.parse_name(os.path.basename(fixture_file))
            open_method, mode = self.compression_formats[cmp_fmt]
            fixture = open_method(fixture_file, mode)
            try:
                try:
                    self.fixture_count += 1
                    objects_in_fixture = 0
                    loaded_objects_in_fixture = 0
                    if self.verbosity >= 2:
                        self.stdout.write(b"Installing %s fixture '%s' from %s." % (
                         ser_fmt, fixture_name, humanize(fixture_dir)))
                    objects = serializers.deserialize(ser_fmt, fixture, using=self.using, ignorenonexistent=self.ignore)
                    for obj in objects:
                        objects_in_fixture += 1
                        if obj.object._meta.app_config in self.excluded_apps or type(obj.object) in self.excluded_models:
                            continue
                        if router.allow_migrate_model(self.using, obj.object.__class__):
                            loaded_objects_in_fixture += 1
                            self.models.add(obj.object.__class__)
                            try:
                                obj.save(using=self.using)
                                if show_progress:
                                    self.stdout.write(b'\rProcessed %i object(s).' % loaded_objects_in_fixture, ending=b'')
                            except (DatabaseError, IntegrityError) as e:
                                e.args = (
                                 b'Could not load %(app_label)s.%(object_name)s(pk=%(pk)s): %(error_msg)s' % {b'app_label': obj.object._meta.app_label, 
                                    b'object_name': obj.object._meta.object_name, 
                                    b'pk': obj.object.pk, 
                                    b'error_msg': force_text(e)},)
                                raise

                    if objects and show_progress:
                        self.stdout.write(b'')
                    self.loaded_object_count += loaded_objects_in_fixture
                    self.fixture_object_count += objects_in_fixture
                except Exception as e:
                    if not isinstance(e, CommandError):
                        e.args = (
                         b"Problem installing fixture '%s': %s" % (fixture_file, e),)
                    raise

            finally:
                fixture.close()

            if objects_in_fixture == 0:
                warnings.warn(b"No fixture data found for '%s'. (File format may be invalid.)" % fixture_name, RuntimeWarning)

    @lru_cache.lru_cache(maxsize=None)
    def find_fixtures(self, fixture_label):
        """
        Finds fixture files for a given label.
        """
        fixture_name, ser_fmt, cmp_fmt = self.parse_name(fixture_label)
        databases = [self.using, None]
        cmp_fmts = list(self.compression_formats.keys()) if cmp_fmt is None else [cmp_fmt]
        ser_fmts = serializers.get_public_serializer_formats() if ser_fmt is None else [ser_fmt]
        if self.verbosity >= 2:
            self.stdout.write(b"Loading '%s' fixtures..." % fixture_name)
        if os.path.isabs(fixture_name):
            fixture_dirs = [
             os.path.dirname(fixture_name)]
            fixture_name = os.path.basename(fixture_name)
        else:
            fixture_dirs = self.fixture_dirs
            if os.path.sep in os.path.normpath(fixture_name):
                fixture_dirs = [ os.path.join(dir_, os.path.dirname(fixture_name)) for dir_ in fixture_dirs ]
                fixture_name = os.path.basename(fixture_name)
            suffixes = ((b'.').join(ext for ext in combo if ext) for combo in product(databases, ser_fmts, cmp_fmts))
            targets = set((b'.').join((fixture_name, suffix)) for suffix in suffixes)
            fixture_files = []
            for fixture_dir in fixture_dirs:
                if self.verbosity >= 2:
                    self.stdout.write(b'Checking %s for fixtures...' % humanize(fixture_dir))
                fixture_files_in_dir = []
                path = os.path.join(fixture_dir, fixture_name)
                for candidate in glob.iglob(glob_escape(path) + b'*'):
                    if os.path.basename(candidate) in targets:
                        fixture_files_in_dir.append((candidate, fixture_dir, fixture_name))

                if self.verbosity >= 2 and not fixture_files_in_dir:
                    self.stdout.write(b"No fixture '%s' in %s." % (
                     fixture_name, humanize(fixture_dir)))
                if len(fixture_files_in_dir) > 1:
                    raise CommandError(b"Multiple fixtures named '%s' in %s. Aborting." % (
                     fixture_name, humanize(fixture_dir)))
                fixture_files.extend(fixture_files_in_dir)

        if not fixture_files:
            raise CommandError(b"No fixture named '%s' found." % fixture_name)
        return fixture_files

    @cached_property
    def fixture_dirs(self):
        """
        Return a list of fixture directories.

        The list contains the 'fixtures' subdirectory of each installed
        application, if it exists, the directories in FIXTURE_DIRS, and the
        current directory.
        """
        dirs = []
        fixture_dirs = settings.FIXTURE_DIRS
        if len(fixture_dirs) != len(set(fixture_dirs)):
            raise ImproperlyConfigured(b'settings.FIXTURE_DIRS contains duplicates.')
        for app_config in apps.get_app_configs():
            app_label = app_config.label
            app_dir = os.path.join(app_config.path, b'fixtures')
            if app_dir in fixture_dirs:
                raise ImproperlyConfigured(b"'%s' is a default fixture directory for the '%s' app and cannot be listed in settings.FIXTURE_DIRS." % (
                 app_dir, app_label))
            if self.app_label and app_label != self.app_label:
                continue
            if os.path.isdir(app_dir):
                dirs.append(app_dir)

        dirs.extend(list(fixture_dirs))
        dirs.append(b'')
        dirs = [ upath(os.path.abspath(os.path.realpath(d))) for d in dirs ]
        return dirs

    def parse_name(self, fixture_name):
        """
        Splits fixture name in name, serialization format, compression format.
        """
        parts = fixture_name.rsplit(b'.', 2)
        if len(parts) > 1 and parts[(-1)] in self.compression_formats:
            cmp_fmt = parts[(-1)]
            parts = parts[:-1]
        else:
            cmp_fmt = None
        if len(parts) > 1:
            if parts[(-1)] in self.serialization_formats:
                ser_fmt = parts[(-1)]
                parts = parts[:-1]
            else:
                raise CommandError(b"Problem installing fixture '%s': %s is not a known serialization format." % (
                 (b'').join(parts[:-1]), parts[(-1)]))
        else:
            ser_fmt = None
        name = (b'.').join(parts)
        return (
         name, ser_fmt, cmp_fmt)


class SingleZipReader(zipfile.ZipFile):

    def __init__(self, *args, **kwargs):
        zipfile.ZipFile.__init__(self, *args, **kwargs)
        if len(self.namelist()) != 1:
            raise ValueError(b'Zip-compressed fixtures must contain one file.')

    def read(self):
        return zipfile.ZipFile.read(self, self.namelist()[0])


def humanize(dirname):
    if dirname:
        return b"'%s'" % dirname
    return b'absolute path'