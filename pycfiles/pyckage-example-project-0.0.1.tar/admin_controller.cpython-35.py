# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /MyWork/Projects/PyCK/pyck/ext/admin_controller.py
# Compiled at: 2016-01-30 09:20:22
# Size of source mod 2**32: 12087 bytes
__doc__ = '\nPyCK Admin Extension\n====================\n\nAdmin extension that automtically creates CRUD interfaces for all database models\n(or a selected list of models)\n\n'
import os.path
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
import pyck
from pyck.forms import model_form
from pyck.lib.models import get_columns, get_model_record_counts, models_dict_to_list
from pyck.controllers import CRUDController, add_crud_handler
import logging
log = logging.getLogger(__name__)

def add_admin_handler(config, db_session, models=None, route_name_prefix='', url_pattern_prefix='', handler_class=None):
    """
    A utility function to quickly add all admin related routes and set them to the admin handler class with one function call,
    for example::

        from pyck.ext import add_admin_handler, AdminController
        from pyck.lib import get_models
        import my_application_package_name_here

        # Place this with the config.add_route calls
        add_admin_handler(config, db, get_models(my_application_package_name_here), 'admin', '/admin',
                          AdminController)

    :param config:
        The application config object

    :param db:
        The database session object

    :param models:
        Note: For backward compatibility this parameter can either be a list (old) or a dictionary (new).
        List/Dictionary of models for to include in the admin panel.
        get_models function can be used to include all models.

    :param route_name_prefix:
        Optional string prefix to add to all route names generated inside the admin panel.

    :param url_pattern_prefix:
        Optional string prefix to add to all admin section related url patterns

    :param handler_class:
        The AdminController handler class.

    """
    handler_class.db_session = db_session
    handler_class.models = models
    all_models = models_dict_to_list(models)
    for model in all_models:
        handler_class.table_models[model.__tablename__] = model

    handler_class.route_prefix = route_name_prefix
    config.add_route(route_name_prefix + 'admin_index', url_pattern_prefix + '/')
    config.add_view(handler_class, attr='index', route_name=route_name_prefix + 'admin_index', renderer='pyck:templates/admin/index.mako')
    if all_models:
        for model in all_models:
            add_edit_field_args = {}
            list_field_args = {}
            FK_cols = get_columns(model, 'foreign_key')
            for FK in FK_cols:
                db_col = list(FK.foreign_keys)[0].column.name
                display_col = db_col
                db_col_python_type = None
                try:
                    db_col_python_type = list(FK.foreign_keys)[0].column.table.columns[db_col].type.python_type
                except:
                    pass

                if int == db_col_python_type:
                    table_cols = list(list(FK.foreign_keys)[0].column.table.columns.keys())
                    d_idx = table_cols.index(db_col) + 1
                    if len(table_cols) > d_idx:
                        display_col = table_cols[d_idx]
                    db_col = list(FK.foreign_keys)[0].column.table.columns[db_col]
                    display_col = list(FK.foreign_keys)[0].column.table.columns[display_col]
                    add_edit_field_args[FK.name] = dict(choices_fields=[db_col, display_col])
                    for RS in model.__mapper__.relationships:
                        r_col = list(RS.local_columns)[0]
                        if r_col.name == FK.name:
                            list_field_args[FK.name] = dict(display_field='%s.%s' % (RS.key, display_col.name))
                            break

            CC = type(model.__name__ + 'CRUDController', (pyck.controllers.CRUDController,), {'model': model, 'db_session': db_session, 
             'base_template': handler_class.base_template, 
             'add_edit_field_args': add_edit_field_args, 
             'list_field_args': list_field_args, 
             'fetch_record_count': handler_class.display_record_count, 
             'template_extra_params': {'models': models, 
                                       'route_prefix': route_name_prefix, 
                                       'display_record_count': handler_class.display_record_count}})
            props = [i for i in dir(handler_class) if not callable(getattr(handler_class, i)) and i.startswith('crud_')]
            for extra_action in props:
                if model.__name__ in getattr(handler_class, extra_action):
                    setattr(CC, extra_action[5:], getattr(handler_class, extra_action)[model.__name__])

            add_crud_handler(config, route_name_prefix + model.__name__, url_pattern_prefix + '/' + model.__tablename__, CC)


class AdminController(object):
    """AdminController"""
    models = None
    table_models = {}
    db_session = None
    route_prefix = ''
    base_template = 'pyck:templates/admin/admin_base.mako'
    display_record_count = True
    crud_list_sort_by = {}
    crud_list_only = {}
    crud_list_exclude = {}
    crud_models_field_args = {}
    crud_list_actions = {}
    crud_list_per_record_actions = {}
    crud_detail_actions = {}
    crud_detail_exclude = {}

    def __init__(self, request):
        self.request = request
        if self.db_session is None:
            raise ValueError('Must provide a SQLAlchemy database session object as db_session')

    def index(self):
        """Home page"""
        record_counts = None
        if self.display_record_count:
            record_counts = get_model_record_counts(self.db_session, models_dict_to_list(self.models))
        return {'base_template': self.base_template, 'route_prefix': self.route_prefix, 
         'models': self.models, 'db_session': self.db_session, 
         'model_record_counts': record_counts}