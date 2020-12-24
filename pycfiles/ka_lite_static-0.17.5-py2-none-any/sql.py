# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/sql.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import codecs, os, re
from django.conf import settings
from django.core.management.base import CommandError
from django.db import models
from django.db.models import get_models
from django.utils._os import upath

def sql_create(app, style, connection):
    """Returns a list of the CREATE TABLE SQL statements for the given app."""
    if connection.settings_dict[b'ENGINE'] == b'django.db.backends.dummy':
        raise CommandError(b"Django doesn't know which syntax to use for your SQL statements,\n" + b"because you haven't properly specified the ENGINE setting for the database.\n" + b'see: https://docs.djangoproject.com/en/dev/ref/settings/#databases')
    app_models = models.get_models(app, include_auto_created=True)
    final_output = []
    tables = connection.introspection.table_names()
    known_models = set([ model for model in connection.introspection.installed_models(tables) if model not in app_models ])
    pending_references = {}
    for model in app_models:
        output, references = connection.creation.sql_create_model(model, style, known_models)
        final_output.extend(output)
        for refto, refs in references.items():
            pending_references.setdefault(refto, []).extend(refs)
            if refto in known_models:
                final_output.extend(connection.creation.sql_for_pending_references(refto, style, pending_references))

        final_output.extend(connection.creation.sql_for_pending_references(model, style, pending_references))
        known_models.add(model)

    not_installed_models = set(pending_references.keys())
    if not_installed_models:
        alter_sql = []
        for model in not_installed_models:
            alter_sql.extend([ b'-- ' + sql for sql in connection.creation.sql_for_pending_references(model, style, pending_references)
                             ])

        if alter_sql:
            final_output.append(b'-- The following references should be added but depend on non-existent tables:')
            final_output.extend(alter_sql)
    return final_output


def sql_delete(app, style, connection):
    """Returns a list of the DROP TABLE SQL statements for the given app."""
    try:
        cursor = connection.cursor()
    except:
        cursor = None

    if cursor:
        table_names = connection.introspection.table_names(cursor)
    else:
        table_names = []
    output = []
    to_delete = set()
    references_to_delete = {}
    app_models = models.get_models(app, include_auto_created=True)
    for model in app_models:
        if cursor and connection.introspection.table_name_converter(model._meta.db_table) in table_names:
            opts = model._meta
            for f in opts.local_fields:
                if f.rel and f.rel.to not in to_delete:
                    references_to_delete.setdefault(f.rel.to, []).append((model, f))

            to_delete.add(model)

    for model in app_models:
        if connection.introspection.table_name_converter(model._meta.db_table) in table_names:
            output.extend(connection.creation.sql_destroy_model(model, references_to_delete, style))

    if cursor:
        cursor.close()
        connection.close()
    return output[::-1]


def sql_flush(style, connection, only_django=False, reset_sequences=True):
    """
    Returns a list of the SQL statements used to flush the database.

    If only_django is True, then only table names that have associated Django
    models and are in INSTALLED_APPS will be included.
    """
    if only_django:
        tables = connection.introspection.django_table_names(only_existing=True)
    else:
        tables = connection.introspection.table_names()
    seqs = connection.introspection.sequence_list() if reset_sequences else ()
    statements = connection.ops.sql_flush(style, tables, seqs)
    return statements


def sql_custom(app, style, connection):
    """Returns a list of the custom table modifying SQL statements for the given app."""
    output = []
    app_models = get_models(app)
    for model in app_models:
        output.extend(custom_sql_for_model(model, style, connection))

    return output


def sql_indexes(app, style, connection):
    """Returns a list of the CREATE INDEX SQL statements for all models in the given app."""
    output = []
    for model in models.get_models(app):
        output.extend(connection.creation.sql_indexes_for_model(model, style))

    return output


def sql_all(app, style, connection):
    """Returns a list of CREATE TABLE SQL, initial-data inserts, and CREATE INDEX SQL for the given module."""
    return sql_create(app, style, connection) + sql_custom(app, style, connection) + sql_indexes(app, style, connection)


def _split_statements(content):
    comment_re = re.compile(b"^((?:'[^']*'|[^'])*?)--.*$")
    statements = []
    statement = []
    for line in content.split(b'\n'):
        cleaned_line = comment_re.sub(b'\\1', line).strip()
        if not cleaned_line:
            continue
        statement.append(cleaned_line)
        if cleaned_line.endswith(b';'):
            statements.append((b' ').join(statement))
            statement = []

    return statements


def custom_sql_for_model(model, style, connection):
    opts = model._meta
    app_dir = os.path.normpath(os.path.join(os.path.dirname(upath(models.get_app(model._meta.app_label).__file__)), b'sql'))
    output = []
    if opts.managed:
        post_sql_fields = [ f for f in opts.local_fields if hasattr(f, b'post_create_sql') ]
        for f in post_sql_fields:
            output.extend(f.post_create_sql(style, model._meta.db_table))

    backend_name = connection.settings_dict[b'ENGINE'].split(b'.')[(-1)]
    sql_files = [os.path.join(app_dir, b'%s.%s.sql' % (opts.object_name.lower(), backend_name)),
     os.path.join(app_dir, b'%s.sql' % opts.object_name.lower())]
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            with codecs.open(sql_file, b'U', encoding=settings.FILE_CHARSET) as (fp):
                output.extend(_split_statements(fp.read()))

    return output


def emit_post_sync_signal(created_models, verbosity, interactive, db):
    for app in models.get_apps():
        app_name = app.__name__.split(b'.')[(-2)]
        if verbosity >= 2:
            print b'Running post-sync handlers for application %s' % app_name
        models.signals.post_syncdb.send(sender=app, app=app, created_models=created_models, verbosity=verbosity, interactive=interactive, db=db)