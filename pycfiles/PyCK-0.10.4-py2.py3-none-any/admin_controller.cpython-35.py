# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /MyWork/Projects/PyCK/pyck/ext/admin_controller.py
# Compiled at: 2016-01-30 09:20:22
# Size of source mod 2**32: 12087 bytes
"""
PyCK Admin Extension
====================

Admin extension that automtically creates CRUD interfaces for all database models
(or a selected list of models)

"""
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
    __doc__ = '\n    Enables automatic Admin interface generation from database models.\n    The :class:`pyck.ext.admin_controller.AdminController` allows you to quickly enable Admin interface for any number\n    of database models you like. To use AdminController at minimum these steps must be followed.\n\n\n    1. In your application\'s routes settings, specify the url where the CRUD interface should be displayed. You can use\n    the :func:`pyck.ext.admin_controller.add_admin_handler` function for it. For example in your __init__.py; put code\n    like::\n\n        from pyck.ext import AdminController, add_admin_handler\n        from pyck.lib import get_models\n        import my_application_package_name_here\n\n        # Place this with the config.add_route calls\n        add_admin_handler(config, db, get_models(my_application_package_name_here), \'admin\', \'/admin\',\n                          AdminController)\n\n    and that\'s all you need to do to get a fully operation Admin interface.\n\n    **Configuration Options**\n\n    These parameters are to be set as class properties in a sub-class of AdminController\n\n    :param display_record_count:\n        Boolean value controlling if record count is to be displayed next to the menu items for CRUD models\n\n    :param crud_list_sort_by:\n        Sort by specs for models.\n\n        Example::\n\n            crud_list_sort_by = {\n                Post.__name__: Post.created.desc()\n            }\n\n    :param crud_models_field_args:\n        A dictionary with key being the model name and value being the field args value for that model.\n\n        Example::\n\n            model_field_args = {\n                \'Product\': {\n                    \'category_id\' : {\'widget\' : Select()}\n                },\n                \'Category\': {\n                    \'description\' : {\'widget\' : TextArea()}\n                },\n            }\n\n    :param crud_list_only:\n        A dictionary containing list of fields to be displayed (and not displaying any other fields) on the record listing page for a specific CRUD model\n\n        Example::\n\n            crud_list_only = {\n                User.__name__: [\'user_id\', \'email\']\n            }\n\n    :param crud_list_exclude:\n        A dictionary containing list of fields not to be displayed on the record listing page for a specific CRUD model\n\n        Example::\n\n            crud_list_exclude = {\n                User.__name__: [\'id\', \'comments\']\n            }\n\n    :param crud_list_actions:\n        A dictionary containing list of actions to be displayed on the record listing page for a specific CRUD model\n\n        Example::\n\n            crud_list_actions = {\n                User.__name__: [\n                    {\'link_text\': \'{friendly_name} popularity graph\', \'link_url\': \'/pop_graph\', \'css_class\': \'btn btn-primary\'},\n                ]\n            }\n\n    :param crud_list_per_record_actions:\n        A dictionary containing list of actions to be displayed next to each record in record listing for a specific CRUD model\n\n        Example::\n\n            crud_list_per_record_actions = {\n                User.__name__: [\n                    {\'link_text\': \'Details\', \'link_url\': \'details/{PK}\'},\n                    {\'link_text\': \'Edit\', \'link_url\': \'edit/{PK}\'},\n                    {\'link_text\': \'Delete\', \'link_url\': \'delete/{PK}\'},\n                    {\'link_text\': \'Upload Photo\', \'link_url\': \'/photo_upload/user/{PK}\'},\n                ]\n            }\n\n    :param crud_list_filter_condition:\n        A SQLAlchemy filter condition to be applied for to the listing page\n\n        Example::\n\n            crud_list_filter_condition = {\n                UserFiles.__name__: "self.model.user_id == self.request.session.get(\'logged_in_user\', \'\')"\n            }\n\n    :param crud_detail_exclude:\n        A dictionary containing list of fields not to be displayed on the record details page for a specific CRUD model\n\n        Example::\n\n            crud_detail_exclude = {\n                User.__name__: [\'id\', \'comments\']\n            }\n\n    :param crud_detail_actions:\n        A dictionary containing list of actions to be displayed on the details view page of a specific CRUD model\n\n        Example::\n\n            crud_list_per_record_actions = {\n                User.__name__: [\n                    {\'link_text\': \'Details\', \'link_url\': \'details/{PK}\'},\n                    {\'link_text\': \'Edit\', \'link_url\': \'edit/{PK}\'},\n                    {\'link_text\': \'Delete\', \'link_url\': \'delete/{PK}\'},\n                    {\'link_text\': \'Upload Photo\', \'link_url\': \'/photo_upload/user/{PK}\'},\n                ]\n            }\n\n    ** TODO **\n\n    * More documentation of various options and methods\n    * An AdminController tutorial\n    * Tests for the controller\n    * Add support for composite primary keys\n\n    '
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