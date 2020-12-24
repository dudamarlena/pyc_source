# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/migrations/recorder.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.apps.registry import Apps
from django.db import models
from django.db.utils import DatabaseError
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from .exceptions import MigrationSchemaMissing

class MigrationRecorder(object):
    """
    Deals with storing migration records in the database.

    Because this table is actually itself used for dealing with model
    creation, it's the one thing we can't do normally via migrations.
    We manually handle table creation/schema updating (using schema backend)
    and then have a floating model to do queries with.

    If a migration is unapplied its row is removed from the table. Having
    a row in the table always means a migration is applied.
    """

    @python_2_unicode_compatible
    class Migration(models.Model):
        app = models.CharField(max_length=255)
        name = models.CharField(max_length=255)
        applied = models.DateTimeField(default=now)

        class Meta:
            apps = Apps()
            app_label = b'migrations'
            db_table = b'django_migrations'

        def __str__(self):
            return b'Migration %s for %s' % (self.name, self.app)

    def __init__(self, connection):
        self.connection = connection

    @property
    def migration_qs(self):
        return self.Migration.objects.using(self.connection.alias)

    def ensure_schema(self):
        """
        Ensures the table exists and has the correct schema.
        """
        if self.Migration._meta.db_table in self.connection.introspection.table_names(self.connection.cursor()):
            return
        try:
            with self.connection.schema_editor() as (editor):
                editor.create_model(self.Migration)
        except DatabaseError as exc:
            raise MigrationSchemaMissing(b'Unable to create the django_migrations table (%s)' % exc)

    def applied_migrations(self):
        """
        Returns a set of (app, name) of applied migrations.
        """
        self.ensure_schema()
        return set(tuple(x) for x in self.migration_qs.values_list(b'app', b'name'))

    def record_applied(self, app, name):
        """
        Records that a migration was applied.
        """
        self.ensure_schema()
        self.migration_qs.create(app=app, name=name)

    def record_unapplied(self, app, name):
        """
        Records that a migration was unapplied.
        """
        self.ensure_schema()
        self.migration_qs.filter(app=app, name=name).delete()

    def flush(self):
        """
        Deletes all migration records. Useful if you're testing migrations.
        """
        self.migration_qs.all().delete()