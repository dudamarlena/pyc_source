# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /MyWork/Projects/PyCK/pyck/controllers/crud_controller.py
# Compiled at: 2017-03-22 14:04:28
# Size of source mod 2**32: 29073 bytes
import json, os.path
from sqlalchemy import func, or_
from sqlalchemy import BIGINT, BINARY, BLOB, BOOLEAN, BigInteger, Binary, Boolean, DATE, DATETIME, DECIMAL, Date, DateTime, FLOAT, Float, INT, INTEGER, Integer, Interval, LargeBinary, NUMERIC, Numeric, REAL, SMALLINT, SmallInteger, TIME, TIMESTAMP, Time, VARBINARY, VARCHAR, UnicodeText, Unicode, String, TEXT, Text, NCHAR, NVARCHAR, CHAR, CLOB
from sqlalchemy.exc import IntegrityError
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotAcceptable
from wtforms.widgets.core import Select
from wtforms import SelectField
from wtdojo.fields.core import DojoSelectField
from wtforms import validators
from pyck.forms import model_form, dojo_model_form
from pyck.lib.pagination import get_pages
from pyck.lib.models import get_columns, get_model_record_counts, models_dict_to_list
from pyck.lib import dates_and_times
import csv
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import logging
log = logging.getLogger(__name__)

def add_crud_handler(config, route_name_prefix='', url_pattern_prefix='', handler_class=None):
    """
    A utility function to quickly add all crud related routes and set them to the crud handler class with one function
    call, for example::

        from pyck.controllers import add_crud_handler
        from controllers.views import WikiCRUDController
        .
        .
        .
        add_crud_handler(config, APP_NAME + '.', '/crud', WikiCRUDController)

    :param config:
        The application config object
    :param route_name_prefix:
        Optional string prefix to add to all route names. Useful if you're adding multiple CRUD controllers and want to
        avoid route name conflicts.
    :param url_pattern_prefix:
        Optional string prefix to add to all crud related url patterns
    :param handler_class:
        The handler class that is used to handle CRUD requests. Must be sub-class of :class:`pyck.controllers.CRUDController`

    """
    config.add_route(route_name_prefix + 'CRUD_list', url_pattern_prefix + '/')
    config.add_view(handler_class, attr='list', route_name=route_name_prefix + 'CRUD_list', renderer='pyck:templates/crud/list.mako')
    config.add_route(route_name_prefix + 'CRUD_list_csv', url_pattern_prefix + '/csv')
    config.add_view(handler_class, attr='list_csv', route_name=route_name_prefix + 'CRUD_list_csv')
    config.add_route(route_name_prefix + 'CRUD_add', url_pattern_prefix + '/add')
    config.add_view(handler_class, attr='add', route_name=route_name_prefix + 'CRUD_add', renderer='pyck:templates/crud/add_or_edit.mako')
    config.add_route(route_name_prefix + 'CRUD_edit', url_pattern_prefix + '/edit/{PK}')
    config.add_view(handler_class, attr='edit', route_name=route_name_prefix + 'CRUD_edit', renderer='pyck:templates/crud/add_or_edit.mako')
    config.add_route(route_name_prefix + 'CRUD_details', url_pattern_prefix + '/details/{PK}')
    config.add_view(handler_class, attr='details', route_name=route_name_prefix + 'CRUD_details', renderer='pyck:templates/crud/details.mako')
    config.add_route(route_name_prefix + 'CRUD_delete', url_pattern_prefix + '/delete/{PK}')
    config.add_view(handler_class, attr='delete', route_name=route_name_prefix + 'CRUD_delete')


class CRUDController(object):
    """CRUDController"""
    model = None
    friendly_name = None
    db_session = None
    add_edit_exclude = None
    add_edit_field_args = {}
    list_sort_by = None
    list_recs_per_page = 10
    list_max_pages = 10
    list_field_args = {}
    list_only = None
    list_exclude = None
    detail_exclude = None
    list_filter_condition = None
    list_actions = [
     {'link_text': 'Add {friendly_name}', 'link_url': 'add', 'css_class': 'btn btn-success'}]
    list_per_record_actions = [
     {'link_text': 'Details', 'link_url': 'details/{PK}'},
     {'link_text': 'Edit', 'link_url': 'edit/{PK}'},
     {'link_text': 'Delete', 'link_url': 'delete/{PK}', 'css_class': 'text-danger'}]
    detail_actions = [
     {'link_text': 'Edit', 'link_url': '../edit/{PK}'},
     {'link_text': 'Delete', 'link_url': '../delete/{PK}', 'css_class': 'btn btn-danger'}]
    field_translations = {}
    base_template = '/base.mako'
    template_extra_params = {}
    fetch_record_count = False
    enable_csv = True

    def __init__(self, request):
        self.request = request
        if self.db_session is None:
            raise ValueError('Must provide a SQLAlchemy database session object as db_session')
        if self.friendly_name is None:
            self.friendly_name = self.model.__tablename__.replace('_', ' ').title()

    def _get_rec_from_pk_val(self):
        pk_val = self.request.matchdict.get('PK')
        pk_name = ''
        R = None
        primary_key_columns = list(self.model.__table__.primary_key.columns.keys())
        if len(primary_key_columns) > 1:
            pass
        else:
            pk_name = primary_key_columns[0]
            R = self.db_session.query(self.model).filter('%s=:pk_val' % pk_name).params(pk_val=pk_val).one()
        return R

    def _get_modelform_field_args(self):
        """
        Returns only the fields that can be passed on to the ModelForm constructor.
        This involves removing the choices and choices_fields keys.
        """
        form_fields = {}
        exclude_keys = [
         'choices', 'choices_fields']
        for field_name, field_data in list(self.add_edit_field_args.items()):
            new_dict = {}
            for k, v in list(field_data.items()):
                if k not in exclude_keys:
                    new_dict[k] = v

            form_fields[field_name] = new_dict

        return form_fields

    def _get_exclude_list(self, action_type):
        if self.add_edit_exclude:
            return self.add_edit_exclude
        log.info('determining exclude list')
        exclude_list = list(self.model.__mapper__.relationships.keys())
        log.info(exclude_list)
        if 'add' == action_type:
            cols = get_columns(self.model, 'primary_key')
            for c in cols:
                if int == c.property.columns[0].type.python_type and 0 == len(c.property.columns[0].foreign_keys):
                    exclude_list.append(c.key)

        return exclude_list

    def _models_rec_count_if_needed(self):
        if self.fetch_record_count and 'models' in self.template_extra_params:
            return get_model_record_counts(self.db_session, models_dict_to_list(self.template_extra_params['models']))
        else:
            return {}

    def _get_search_condition(self, col, val, case_sensitive=True, partial_match=False):
        search_condition = None
        col_type = col.type.__class__
        if col_type in (VARCHAR, UnicodeText, Unicode, String, TEXT, Text, NCHAR, NVARCHAR, CHAR, CLOB):
            if case_sensitive:
                if partial_match:
                    search_condition = col.like('%{}%'.format(val))
                else:
                    search_condition = col == val
            else:
                if partial_match:
                    search_condition = col.ilike('%{}%'.format(val))
                else:
                    search_condition = func.lower(col) == func.lower(val)
        else:
            if col_type in (BOOLEAN, Boolean, Binary):
                if val.lower() in ('0', '1', 'true', 'false'):
                    search_condition = col == val.title()
            else:
                if col_type in (BIGINT, BigInteger, INT, INTEGER, Integer, Interval,
                 NUMERIC, Numeric, SMALLINT, SmallInteger):
                    if val.isdigit():
                        search_condition = col == val
                else:
                    if col_type in (DECIMAL, FLOAT, Float, REAL):
                        if val.replace('.', '').isdigit():
                            search_condition = col == val
                    elif col_type in (DATE, Date):
                        try:
                            date_val = dates_and_times.Date.from_string(val)
                            if partial_match:
                                search_condition = col.between(*date_val.range())
                            elif not date_val.is_partial():
                                search_condition = col == date_val.to_native()
                        except ValueError:
                            pass

        if col_type in (Time, TIME):
            try:
                time_val = dates_and_times.Time.from_string(val)
                if partial_match:
                    search_condition = col.between(*time_val.range())
                elif not time_val.is_partial():
                    search_condition = col == time_val.to_native()
            except ValueError:
                pass

        elif col_type in (DATETIME, DateTime, TIMESTAMP):
            try:
                date_val = dates_and_times.DateTime.from_string(val)
                if partial_match:
                    search_condition = col.between(*date_val.range())
                elif not date_val.is_partial():
                    search_condition = col == date_val.to_native()
            except ValueError:
                pass

            return search_condition

    def _get_list_columns(self):
        columns = []
        if self.list_only is not None:
            columns = self.list_only
        else:
            if self.list_exclude is not None:
                for column in list(self.model.__table__.columns.keys()):
                    if column not in self.list_exclude:
                        columns.append(column)

            else:
                columns = list(self.model.__table__.columns.keys())
        return columns

    def _list_csv_common_code(self, return_only_records=False, return_all_records=False):
        """
        Common logic used by both list and csv methods.

        :param return_only_records: Return all params like current page, record count etc or just the records

        :param return_all_records: return records for the current page on or all records

        """
        p = int(self.request.params.get('p', '1'))
        start_idx = self.list_recs_per_page * (p - 1)
        pk_col = list(self.model.__table__.primary_key.columns.keys())[0]
        pk_col = self.model.__table__.primary_key.columns[pk_col]
        query = self.db_session.query(self.model)
        count_query = self.db_session.query(func.count(pk_col))
        if self.list_filter_condition:
            log.warn(self.list_filter_condition)
            cond = eval(self.list_filter_condition)
            query = query.filter(cond)
            count_query = count_query.filter(cond)
        if self.request.GET.get('q', ''):
            search_conditions = []
            search_term = self.request.GET['q'].strip()
            for k, v in self.request.GET.items():
                if k.startswith('_sf_'):
                    col = getattr(self.model, v)
                    case_sensitive = True
                    partial_match = True
                    if '_so_ci' in self.request.GET:
                        case_sensitive = False
                    if '_so_pm' not in self.request.GET:
                        partial_match = False
                    search_condition = self._get_search_condition(col, search_term, case_sensitive=case_sensitive, partial_match=partial_match)
                    log.error(search_condition)
                    if search_condition is not None:
                        search_conditions.append(search_condition)

            log.warn(search_conditions)
            query = query.filter(or_(*search_conditions))
            count_query = count_query.filter(or_(*search_conditions))
        sort_ascending = self.request.GET.get('sa', None)
        sort_descending = self.request.GET.get('sd', None)
        if sort_ascending:
            query = query.order_by(sort_ascending)
        else:
            if sort_descending:
                query = query.order_by(sort_descending + ' desc')
            elif self.list_sort_by is not None:
                query = query.order_by(self.list_sort_by)
        if not return_all_records:
            query = query.slice(start_idx, start_idx + self.list_recs_per_page)
        records = query
        columns = self._get_list_columns()
        total_recs = count_query.scalar()
        pages = get_pages(total_recs, p, self.list_recs_per_page, self.list_max_pages)
        primary_key_columns = list(self.model.__table__.primary_key.columns.keys())
        if return_only_records:
            return records
        else:
            return {'columns': columns, 'primary_key_columns': primary_key_columns, 
             'records': records, 'pages': pages, 'current_page': p, 
             'total_records': total_recs}

    def list(self):
        """
        The listing view - Lists all the records with pagination
        """
        list_dict = self._list_csv_common_code(return_only_records=False, return_all_records=False)
        ret_dict = {'base_template': self.base_template, 'friendly_name': self.friendly_name, 
         'records_per_page': self.list_recs_per_page, 'list_field_args': self.list_field_args, 
         'field_translations': self.field_translations, 
         'model_record_counts': self._models_rec_count_if_needed(), 
         'actions': self.list_actions, 'per_record_actions': self.list_per_record_actions}
        ret_dict.update(list_dict)
        return dict(list(ret_dict.items()) + list(self.template_extra_params.items()))

    def _get_col_value(self, col_name, R):
        parts = col_name.split('.')
        obj = R
        for p in parts:
            obj = getattr(obj, p)
            if not obj:
                return ''

        return obj

    def list_csv(self):
        """
        The CSV view - Allow download of the data as CSV
        """
        if not self.enable_csv:
            return HTTPNotAcceptable(detail='CSV download disabled')
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        all_records = False
        if 'y' == self.request.GET.get('all', 'n'):
            all_records = True
        records = self._list_csv_common_code(return_only_records=True, return_all_records=all_records)
        if 0 == records.count():
            return HTTPNotAcceptable(detail='No data')
        columns = self._get_list_columns()
        heading_row = []
        for column in columns:
            if self.field_translations and column in self.field_translations and 'header' in self.field_translations[column]:
                heading_row.append(self.field_translations[column]['header'])
            else:
                heading_row.append(column.replace('_', ' ').title())

        csv_writer.writerow(heading_row)
        for R in records:
            data_row = []
            for column in columns:
                if column in self.list_field_args and 'display_field' in self.list_field_args[column]:
                    data_row.append(self._get_col_value(self.list_field_args[column]['display_field'], R))
                else:
                    col_value = getattr(R, column)
                    if self.field_translations and column in self.field_translations:
                        col_value = self.field_translations[column]['translator'](col_value)
                    data_row.append(col_value)

            csv_writer.writerow(data_row)

        headers = {}
        headers['Content-Description'] = self.friendly_name
        headers['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(self.friendly_name)
        headers['Content-Type'] = 'text/csv'
        return Response(body=csv_buffer.getvalue(), headers=headers)

    def _get_add_edit_form(self, action_type, R=None):
        exclude_list = self._get_exclude_list(action_type)
        cols = get_columns(self.model, 'primary_key')
        ModelForm = dojo_model_form(self.model, self.db_session, exclude=exclude_list, field_args=self._get_modelform_field_args())
        print('==> %r' % self.add_edit_field_args)
        for field_name, field_data in list(self.add_edit_field_args.items()):
            field = getattr(ModelForm, field_name)
            if 'choices' in field_data or 'choices_fields' in field_data:
                print(' => making field %s into select list' % field_name)
                field.field_class = DojoSelectField

        if 'edit' == action_type:
            f = ModelForm(self.request.POST, R, request_obj=self.request, use_csrf_protection=True)
        else:
            f = ModelForm(self.request.POST, request_obj=self.request, use_csrf_protection=True)
        for field_name, field_data in list(self.add_edit_field_args.items()):
            field = getattr(f, field_name)
            if 'choices' in field_data:
                if 'coerce' in field_data:
                    field.coerce = field_data['coerce']
                else:
                    field.coerce = int
                field.choices = field_data['choices']
            if 'choices_fields' in field_data:
                recs = self.db_session.query(*field_data['choices_fields']).all()
                table_cols = get_columns(self.model)
                for table_col in table_cols:
                    if table_col.property.columns[0].name == field_name and table_col.property.columns[0].nullable:
                        field.validators = []
                        recs.insert(0, (None, ''))

                field.choices = recs

        return f

    def _redirect(self, location):
        """
        If came_from is set in session, redirects to it's value otherwise
        redirects to the location passed
        """
        if self.request.session.get('came_from', None):
            return HTTPFound(location=self.request.session.get('came_from'))
        else:
            return HTTPFound(location=location)

    def add(self):
        """
        The add record view
        """
        f = self._get_add_edit_form('add')
        if 'POST' == self.request.method and 'form.submitted' in self.request.params:
            obj = self.model()
            for fname, f_field in list(f._fields.items()):
                print('=> Field: %s, %r', fname, f_field)
                print('-> have field in model: %r', hasattr(obj, fname))
                if hasattr(f_field, 'choices') and f_field.data in ('', 'None'):
                    f_field.data = None

            f.populate_obj(obj)
            self.db_session.add(obj)
            self.request.session.flash(self.friendly_name + ' added successfully!')
            return self._redirect(os.path.dirname(self.request.current_route_url()) + '/')
        ret_dict = {'base_template': self.base_template, 'friendly_name': self.friendly_name, 
         'model_record_counts': self._models_rec_count_if_needed(), 
         'form': f, 'action_type': 'add'}
        return dict(list(ret_dict.items()) + list(self.template_extra_params.items()))

    def edit(self):
        """
        The edit and update record view
        """
        R = self._get_rec_from_pk_val()
        f = self._get_add_edit_form('edit', R)
        if 'POST' == self.request.method and 'form.submitted' in self.request.params:
            obj = self.model()
            for fname, f_field in list(f._fields.items()):
                if hasattr(f_field, 'choices') and f_field.data in ('', 'None'):
                    f_field.data = None

            f.populate_obj(R)
            self.request.session.flash(self.friendly_name + ' updated successfully!')
            return self._redirect(os.path.dirname(os.path.dirname(self.request.current_route_url())) + '/')
        ret_dict = {'base_template': self.base_template, 
         'model_record_counts': self._models_rec_count_if_needed(), 
         'friendly_name': self.friendly_name, 'form': f, 'action_type': 'edit'}
        return dict(list(ret_dict.items()) + list(self.template_extra_params.items()))

    def delete(self):
        """
        The record delete view

        TODO:

          * Later may need to add support for composite primary keys here.
        """
        R = self._get_rec_from_pk_val()
        try:
            self.db_session.delete(R)
            self.db_session.flush()
        except IntegrityError as exp:
            return HTTPNotAcceptable(detail='Cannot delete category as it has dependent records\n' + str(exp))

        self.request.session.flash(self.friendly_name + ' deleted successfully!')
        return self._redirect(os.path.dirname(os.path.dirname(self.request.current_route_url())) + '/')

    def details(self):
        """
        The record details view
        """
        R = self._get_rec_from_pk_val()
        columns = list(self.model.__table__.columns.keys())
        if self.detail_exclude:
            columns = [c for c in columns if c not in self.detail_exclude]
        primary_key_columns = list(self.model.__table__.primary_key.columns.keys())
        ret_dict = {'base_template': self.base_template, 'R': R, 
         'friendly_name': self.friendly_name, 
         'model_record_counts': self._models_rec_count_if_needed(), 
         'columns': columns, 'primary_key_columns': primary_key_columns, 
         'actions': self.detail_actions, 
         'field_translations': self.field_translations}
        return dict(list(ret_dict.items()) + list(self.template_extra_params.items()))