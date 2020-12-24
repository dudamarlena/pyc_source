# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/loaddata.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import sys, os, gzip, zipfile
from optparse import make_option
import traceback
from django.conf import settings
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.db import connections, router, transaction, DEFAULT_DB_ALIAS, IntegrityError, DatabaseError
from django.db.models import get_apps
from django.utils.encoding import force_text
from django.utils._os import upath
from itertools import product
try:
    import bz2
    has_bz2 = True
except ImportError:
    has_bz2 = False

class Command(BaseCommand):
    help = b'Installs the named fixture(s) in the database.'
    args = b'fixture [fixture ...]'
    option_list = BaseCommand.option_list + (
     make_option(b'--database', action=b'store', dest=b'database', default=DEFAULT_DB_ALIAS, help=b'Nominates a specific database to load fixtures into. Defaults to the "default" database.'),
     make_option(b'--ignorenonexistent', b'-i', action=b'store_true', dest=b'ignore', default=False, help=b'Ignores entries in the serialized data for fields that do not currently exist on the model.'))

    def handle(self, *fixture_labels, **options):
        ignore = options.get(b'ignore')
        using = options.get(b'database')
        connection = connections[using]
        if not len(fixture_labels):
            raise CommandError(b'No database fixture specified. Please provide the path of at least one fixture in the command line.')
        verbosity = int(options.get(b'verbosity'))
        show_traceback = options.get(b'traceback')
        commit = options.get(b'commit', True)
        fixture_count = 0
        loaded_object_count = 0
        fixture_object_count = 0
        models = set()
        humanize = lambda dirname: b"'%s'" % dirname if dirname else b'absolute path'
        cursor = connection.cursor()
        if commit:
            transaction.commit_unless_managed(using=using)
            transaction.enter_transaction_management(using=using)
            transaction.managed(True, using=using)

        class SingleZipReader(zipfile.ZipFile):

            def __init__(self, *args, **kwargs):
                zipfile.ZipFile.__init__(self, *args, **kwargs)
                assert settings.DEBUG and len(self.namelist()) == 1, b'Zip-compressed fixtures must contain only one file.'

            def read(self):
                return zipfile.ZipFile.read(self, self.namelist()[0])

        compression_types = {None: open, 
           b'gz': gzip.GzipFile, 
           b'zip': SingleZipReader}
        if has_bz2:
            compression_types[b'bz2'] = bz2.BZ2File
        app_module_paths = []
        for app in get_apps():
            if hasattr(app, b'__path__'):
                for path in app.__path__:
                    app_module_paths.append(upath(path))

            else:
                app_module_paths.append(upath(app.__file__))

        app_fixtures = [ os.path.join(os.path.dirname(path), b'fixtures') for path in app_module_paths ]
        try:
            with connection.constraint_checks_disabled():
                for fixture_label in fixture_labels:
                    parts = fixture_label.split(b'.')
                    if len(parts) > 1 and parts[(-1)] in compression_types:
                        compression_formats = [
                         parts[(-1)]]
                        parts = parts[:-1]
                    else:
                        compression_formats = compression_types.keys()
                    if len(parts) == 1:
                        fixture_name = parts[0]
                        formats = serializers.get_public_serializer_formats()
                    else:
                        fixture_name, format = (b'.').join(parts[:-1]), parts[(-1)]
                        if format in serializers.get_public_serializer_formats():
                            formats = [
                             format]
                        else:
                            formats = []
                        if formats:
                            if verbosity >= 2:
                                self.stdout.write(b"Loading '%s' fixtures..." % fixture_name)
                        else:
                            raise CommandError(b"Problem installing fixture '%s': %s is not a known serialization format." % (
                             fixture_name, format))
                        if os.path.isabs(fixture_name):
                            fixture_dirs = [
                             fixture_name]
                        else:
                            fixture_dirs = app_fixtures + list(settings.FIXTURE_DIRS) + [b'']
                        for fixture_dir in fixture_dirs:
                            if verbosity >= 2:
                                self.stdout.write(b'Checking %s for fixtures...' % humanize(fixture_dir))
                            label_found = False
                            for combo in product([using, None], formats, compression_formats):
                                database, format, compression_format = combo
                                file_name = (b'.').join(p for p in [
                                 fixture_name, database, format, compression_format] if p)
                                if verbosity >= 3:
                                    self.stdout.write(b"Trying %s for %s fixture '%s'..." % (
                                     humanize(fixture_dir), file_name, fixture_name))
                                full_path = os.path.join(fixture_dir, file_name)
                                open_method = compression_types[compression_format]
                                try:
                                    fixture = open_method(full_path, b'r')
                                except IOError:
                                    if verbosity >= 2:
                                        self.stdout.write(b"No %s fixture '%s' in %s." % (
                                         format, fixture_name, humanize(fixture_dir)))
                                else:
                                    try:
                                        try:
                                            if label_found:
                                                raise CommandError(b"Multiple fixtures named '%s' in %s. Aborting." % (
                                                 fixture_name, humanize(fixture_dir)))
                                            fixture_count += 1
                                            objects_in_fixture = 0
                                            loaded_objects_in_fixture = 0
                                            if verbosity >= 2:
                                                self.stdout.write(b"Installing %s fixture '%s' from %s." % (
                                                 format, fixture_name, humanize(fixture_dir)))
                                            objects = serializers.deserialize(format, fixture, using=using, ignorenonexistent=ignore)
                                            for obj in objects:
                                                objects_in_fixture += 1
                                                if router.allow_syncdb(using, obj.object.__class__):
                                                    loaded_objects_in_fixture += 1
                                                    models.add(obj.object.__class__)
                                                    try:
                                                        obj.save(using=using)
                                                    except (DatabaseError, IntegrityError) as e:
                                                        e.args = (
                                                         b'Could not load %(app_label)s.%(object_name)s(pk=%(pk)s): %(error_msg)s' % {b'app_label': obj.object._meta.app_label, 
                                                            b'object_name': obj.object._meta.object_name, 
                                                            b'pk': obj.object.pk, 
                                                            b'error_msg': force_text(e)},)
                                                        raise

                                            loaded_object_count += loaded_objects_in_fixture
                                            fixture_object_count += objects_in_fixture
                                            label_found = True
                                        except Exception as e:
                                            if not isinstance(e, CommandError):
                                                e.args = (
                                                 b"Problem installing fixture '%s': %s" % (full_path, e),)
                                            raise

                                    finally:
                                        fixture.close()

                                    if objects_in_fixture == 0:
                                        raise CommandError(b"No fixture data found for '%s'. (File format may be invalid.)" % fixture_name)

            table_names = [ model._meta.db_table for model in models ]
            try:
                connection.check_constraints(table_names=table_names)
            except Exception as e:
                e.args = (
                 b'Problem installing fixtures: %s' % e,)
                raise

        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception as e:
            if commit:
                transaction.rollback(using=using)
                transaction.leave_transaction_management(using=using)
            raise

        if loaded_object_count > 0:
            sequence_sql = connection.ops.sequence_reset_sql(no_style(), models)
            if sequence_sql:
                if verbosity >= 2:
                    self.stdout.write(b'Resetting sequences\n')
                for line in sequence_sql:
                    cursor.execute(line)

        if commit:
            transaction.commit(using=using)
            transaction.leave_transaction_management(using=using)
        if verbosity >= 1:
            if fixture_object_count == loaded_object_count:
                self.stdout.write(b'Installed %d object(s) from %d fixture(s)' % (
                 loaded_object_count, fixture_count))
            else:
                self.stdout.write(b'Installed %d object(s) (of %d) from %d fixture(s)' % (
                 loaded_object_count, fixture_object_count, fixture_count))
        if commit:
            connection.close()
        return