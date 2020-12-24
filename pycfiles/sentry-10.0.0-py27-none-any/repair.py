# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/runner/commands/repair.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import os, click
from contextlib import contextmanager
from django.db import transaction
from sentry.runner.decorators import configuration

class RollbackLocally(Exception):
    pass


@contextmanager
def catchable_atomic():
    try:
        with transaction.atomic():
            yield
    except RollbackLocally:
        pass


def sync_docs():
    click.echo('Forcing documentation sync')
    from sentry.utils.integrationdocs import sync_docs, DOC_FOLDER
    if os.access(DOC_FOLDER, os.W_OK):
        try:
            sync_docs()
        except Exception as e:
            click.echo(' - skipping, failure: %s' % e)

    elif os.path.isdir(DOC_FOLDER):
        click.echo(' - skipping, path cannot be written to: %r' % DOC_FOLDER)
    else:
        click.echo(' - skipping, path does not exist: %r' % DOC_FOLDER)


def create_missing_dsns():
    from sentry.models import Project, ProjectKey
    click.echo('Creating missing DSNs')
    queryset = Project.objects.filter(key_set__isnull=True)
    for project in queryset:
        try:
            ProjectKey.objects.get_or_create(project=project)
        except ProjectKey.MultipleObjectsReturned:
            pass


def fix_group_counters():
    from sentry.models import Activity
    from django.db import connection
    click.echo('Correcting Group.num_comments counter')
    cursor = connection.cursor()
    cursor.execute('\n        UPDATE sentry_groupedmessage SET num_comments = (\n            SELECT COUNT(*) from sentry_activity\n            WHERE type = %s and group_id = sentry_groupedmessage.id\n        )\n    ', [
     Activity.NOTE])


@click.command()
@click.option('--with-docs/--without-docs', default=False, help='Synchronize and repair embedded documentation. This is disabled by default.')
@configuration
def repair(with_docs):
    """Attempt to repair any invalid data.

    This by default will correct some common issues like projects missing
    DSNs or counters desynchronizing.  Optionally it can also synchronize
    the current client documentation from the Sentry documentation server
    (--with-docs).
    """
    if with_docs:
        sync_docs()
    create_missing_dsns()
    fix_group_counters()