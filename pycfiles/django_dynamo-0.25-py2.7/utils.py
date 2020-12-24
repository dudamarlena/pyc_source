# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dynamo\utils.py
# Compiled at: 2011-08-02 15:59:24
from django.db import connection
from django.db import models
from django.db.models.signals import class_prepared
from django.db.models.loading import cache as app_cache
from django.core.urlresolvers import clear_url_caches
from django.utils.importlib import import_module
from django.utils.functional import wraps
from django.conf import settings
from django.contrib.admin.sites import NotRegistered
from django.contrib import admin
from south.db import db

def build_existing_dynamic_models():
    """ Builds all existing dynamic models at once. """
    MetaModel = models.get_model('dynamo', 'MetaModel')
    for meta_model in MetaModel.objects.all():
        DynamicModel = meta_model.get_model()
        create_db_table(DynamicModel)
        add_necessary_db_columns(DynamicModel)


def model_maintenance(update_cache=True, update_admin=True):
    """
    A decorator that takes care of all the admin/app cache activites for all
    underlying db activities.
    """

    def decorator(func):

        def inner(DynamicModel, update_cache=update_cache, update_admin=update_admin):
            if update_cache:
                remove_from_model_cache(DynamicModel._meta.app_label, DynamicModel.__name__)
            if getattr(DynamicModel, 'admin', update_admin):
                unregister_from_admin(admin.site, DynamicModel)
            func(DynamicModel)
            if update_cache:
                add_to_model_cache(DynamicModel, DynamicModel._meta.app_label, DynamicModel.__name__)
            if getattr(DynamicModel, 'admin', update_admin):
                register_in_admin(admin.site, DynamicModel)

        return wraps(func)(inner)

    return decorator


def unregister_from_admin(admin_site, model):
    """
    Removes the dynamic model from the given admin site and clears the
    url cache
    """
    for reg_model in admin_site._registry.keys():
        if model._meta.db_table == reg_model._meta.db_table:
            del admin_site._registry[reg_model]

    try:
        admin_site.unregister(model)
    except NotRegistered:
        pass

    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()


def register_in_admin(admin_site, model, admin_class=None):
    """
    Registers the dynamic model with the given admin site and clears the
    url cache
    """
    admin_site.register(model, admin_class)
    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()


def add_to_model_cache(model, app_label, model_name):
    """
    Adds any given model to django's model cache
    """
    app_cache.app_models[app_label.lower()][model_name] = model


def remove_from_model_cache(app_label, model_name):
    """
    Removes any given model to django's model cache
    """
    try:
        del app_cache.app_models[app_label.lower()][model_name]
    except KeyError:
        pass


@model_maintenance()
def create_db_table(model_class):
    """
    Takes a Django model class and create a database table, if necessary.
    """
    db.start_transaction()
    table_name = model_class._meta.db_table
    if connection.introspection.table_name_converter(table_name) not in connection.introspection.table_names():
        fields = _get_fields(model_class)
        db.create_table(table_name, fields)
        db.execute_deferred_sql()
    db.commit_transaction()


@model_maintenance()
def delete_db_table(model_class):
    """
    Takes a Django model class and deletes the database table.
    """
    table_name = model_class._meta.db_table
    db.start_transaction()
    db.delete_table(table_name)
    db.commit_transaction()


def _get_fields(model_class):
    """ Return a list of fields that require table columns. """
    return [ (f.name, f) for f in model_class._meta.local_fields ]


@model_maintenance()
def add_necessary_db_columns(model_class):
    """
    Takes a Django model class and creates relevant columns as necessary based
    on the model_class. No columns or data are renamed or removed.
    This is available in case a database exception occurs.
    """
    db.start_transaction()
    table_name = model_class._meta.db_table
    fields = _get_fields(model_class)
    db_column_names = [ row[0] for row in connection.introspection.get_table_description(connection.cursor(), table_name) ]
    for field_name, field in fields:
        if field.column not in db_column_names:
            try:
                db.add_column(table_name, field_name, field)
            except ValueError:
                field.null = True
                db.add_column(table_name, field_name, field)

    db.execute_deferred_sql()
    db.commit_transaction()


@model_maintenance()
def rename_db_column(model_class, old_name, new_name):
    """
    Takes a Django model class and renames the database columns of the underlying
    talbe as specified.
    """
    table_name = model_class._meta.db_table
    db.start_transaction()
    db.rename_column(table_name, old_name, new_name)
    db.commit_transaction()