# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/flask_admin/model/base.py
# Compiled at: 2016-06-26 14:14:34
import warnings, re, csv, mimetypes, time
from math import ceil
from werkzeug import secure_filename
from flask import current_app, request, redirect, flash, abort, json, Response, get_flashed_messages, stream_with_context
from jinja2 import contextfunction
try:
    import tablib
except ImportError:
    tablib = None

from wtforms.fields import HiddenField
from wtforms.fields.core import UnboundField
from wtforms.validators import ValidationError, InputRequired
from flask_admin.babel import gettext
from flask_admin.base import BaseView, expose
from flask_admin.form import BaseForm, FormOpts, rules
from flask_admin.model import filters, typefmt, template
from flask_admin.actions import ActionsMixin
from flask_admin.helpers import get_form_data, validate_form_on_submit, get_redirect_target, flash_errors
from flask_admin.tools import rec_getattr
from flask_admin._backwards import ObsoleteAttr
from flask_admin._compat import iteritems, itervalues, OrderedDict, as_unicode, csv_encode, text_type
from .helpers import prettify_name, get_mdict_item_or_list
from .ajax import AjaxModelLoader
filter_char_re = re.compile('[^a-z0-9 ]')
filter_compact_re = re.compile(' +')

class ViewArgs(object):
    """
        List view arguments.
    """

    def __init__(self, page=None, sort=None, sort_desc=None, search=None, filters=None, extra_args=None):
        self.page = page
        self.sort = sort
        self.sort_desc = bool(sort_desc)
        self.search = search
        self.filters = filters
        if not self.search:
            self.search = None
        self.extra_args = extra_args or dict()
        return

    def clone(self, **kwargs):
        if self.filters:
            flt = list(self.filters)
        else:
            flt = None
        kwargs.setdefault('page', self.page)
        kwargs.setdefault('sort', self.sort)
        kwargs.setdefault('sort_desc', self.sort_desc)
        kwargs.setdefault('search', self.search)
        kwargs.setdefault('filters', flt)
        kwargs.setdefault('extra_args', dict(self.extra_args))
        return ViewArgs(**kwargs)


class FilterGroup(object):

    def __init__(self, label):
        self.label = label
        self.filters = []

    def append(self, filter):
        self.filters.append(filter)

    def non_lazy(self):
        filters = []
        for item in self.filters:
            copy = dict(item)
            copy['operation'] = as_unicode(copy['operation'])
            options = copy['options']
            if options:
                copy['options'] = [ (k, text_type(v)) for k, v in options ]
            filters.append(copy)

        return (
         as_unicode(self.label), filters)

    def __iter__(self):
        return iter(self.filters)


class BaseModelView(BaseView, ActionsMixin):
    """
        Base model view.

        This view does not make any assumptions on how models are stored or managed, but expects the following:

            1. The provided model is an object
            2. The model contains properties
            3. Each model contains an attribute which uniquely identifies it (i.e. a primary key for a database model)
            4. It is possible to retrieve a list of sorted models with pagination applied from a data source
            5. You can get one model by its identifier from the data source

        Essentially, if you want to support a new data store, all you have to do is:

            1. Derive from the `BaseModelView` class
            2. Implement various data-related methods (`get_list`, `get_one`, `create_model`, etc)
            3. Implement automatic form generation from the model representation (`scaffold_form`)
    """
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = False
    can_export = False
    list_template = 'admin/model/list.html'
    edit_template = 'admin/model/edit.html'
    create_template = 'admin/model/create.html'
    details_template = 'admin/model/details.html'
    edit_modal_template = 'admin/model/modals/edit.html'
    create_modal_template = 'admin/model/modals/create.html'
    details_modal_template = 'admin/model/modals/details.html'
    edit_modal = False
    create_modal = False
    details_modal = False
    column_list = ObsoleteAttr('column_list', 'list_columns', None)
    column_exclude_list = ObsoleteAttr('column_exclude_list', 'excluded_list_columns', None)
    column_details_list = None
    column_details_exclude_list = None
    column_export_list = None
    column_export_exclude_list = None
    column_formatters = ObsoleteAttr('column_formatters', 'list_formatters', dict())
    column_formatters_export = None
    column_type_formatters = ObsoleteAttr('column_type_formatters', 'list_type_formatters', None)
    column_type_formatters_export = None
    column_labels = ObsoleteAttr('column_labels', 'rename_columns', None)
    column_descriptions = None
    column_sortable_list = ObsoleteAttr('column_sortable_list', 'sortable_columns', None)
    column_default_sort = None
    column_searchable_list = ObsoleteAttr('column_searchable_list', 'searchable_columns', None)
    column_editable_list = None
    column_choices = None
    column_filters = None
    named_filter_urls = False
    column_display_pk = ObsoleteAttr('column_display_pk', 'list_display_pk', False)
    column_display_actions = True
    column_extra_row_actions = None
    simple_list_pager = False
    form = None
    form_base_class = BaseForm
    form_args = None
    form_columns = None
    form_excluded_columns = ObsoleteAttr('form_excluded_columns', 'excluded_form_columns', None)
    form_overrides = None
    form_widget_args = None
    form_extra_fields = None
    form_ajax_refs = None
    form_rules = None
    form_edit_rules = None
    form_create_rules = None
    action_disallowed_list = ObsoleteAttr('action_disallowed_list', 'disallowed_actions', [])
    export_max_rows = 0
    export_types = [
     'csv']
    page_size = 20

    def __init__(self, model, name=None, category=None, endpoint=None, url=None, static_folder=None, menu_class_name=None, menu_icon_type=None, menu_icon_value=None):
        """
            Constructor.

            :param model:
                Model class
            :param name:
                View name. If not provided, will use the model class name
            :param category:
                View category
            :param endpoint:
                Base endpoint. If not provided, will use the model name.
            :param url:
                Base URL. If not provided, will use endpoint as a URL.
            :param menu_class_name:
                Optional class name for the menu item.
            :param menu_icon_type:
                Optional icon. Possible icon types:

                 - `flask_admin.consts.ICON_TYPE_GLYPH` - Bootstrap glyph icon
                 - `flask_admin.consts.ICON_TYPE_FONT_AWESOME` - Font Awesome icon
                 - `flask_admin.consts.ICON_TYPE_IMAGE` - Image relative to Flask static directory
                 - `flask_admin.consts.ICON_TYPE_IMAGE_URL` - Image with full URL
            :param menu_icon_value:
                Icon glyph name or URL, depending on `menu_icon_type` setting
        """
        self.model = model
        if name is None:
            name = '%s' % self._prettify_class_name(model.__name__)
        super(BaseModelView, self).__init__(name, category, endpoint, url, static_folder, menu_class_name=menu_class_name, menu_icon_type=menu_icon_type, menu_icon_value=menu_icon_value)
        self.init_actions()
        self._refresh_cache()
        return

    def _get_endpoint(self, endpoint):
        if endpoint:
            return super(BaseModelView, self)._get_endpoint(endpoint)
        return self.model.__name__.lower()

    def _refresh_forms_cache(self):
        self._form_ajax_refs = self._process_ajax_references()
        if self.form_widget_args is None:
            self.form_widget_args = {}
        self._create_form_class = self.get_create_form()
        self._edit_form_class = self.get_edit_form()
        self._delete_form_class = self.get_delete_form()
        if self.column_editable_list:
            self._list_form_class = self.get_list_form()
        else:
            self.column_editable_list = {}
        return

    def _refresh_filters_cache(self):
        self._filters = self.get_filters()
        if self._filters:
            self._filter_groups = OrderedDict()
            self._filter_args = {}
            for i, flt in enumerate(self._filters):
                key = as_unicode(flt.name)
                if key not in self._filter_groups:
                    self._filter_groups[key] = FilterGroup(flt.name)
                self._filter_groups[key].append({'index': i, 
                   'arg': self.get_filter_arg(i, flt), 
                   'operation': flt.operation(), 
                   'options': flt.get_options(self) or None, 
                   'type': flt.data_type})
                self._filter_args[self.get_filter_arg(i, flt)] = (
                 i, flt)

        else:
            self._filter_groups = None
            self._filter_args = None
        return

    def _refresh_form_rules_cache(self):
        if self.form_create_rules:
            self._form_create_rules = rules.RuleSet(self, self.form_create_rules)
        else:
            self._form_create_rules = None
        if self.form_edit_rules:
            self._form_edit_rules = rules.RuleSet(self, self.form_edit_rules)
        else:
            self._form_edit_rules = None
        if self.form_rules:
            form_rules = rules.RuleSet(self, self.form_rules)
            if not self._form_create_rules:
                self._form_create_rules = form_rules
            if not self._form_edit_rules:
                self._form_edit_rules = form_rules
        return

    def _refresh_cache(self):
        """
            Refresh various cached variables.
        """
        self._list_columns = self.get_list_columns()
        self._sortable_columns = self.get_sortable_columns()
        self._details_columns = self.get_details_columns()
        self._export_columns = self.get_export_columns()
        if self.column_labels is None:
            self.column_labels = {}
        self._refresh_forms_cache()
        self._search_supported = self.init_search()
        if self.column_choices:
            self._column_choices_map = dict([ (column, dict(choices)) for column, choices in self.column_choices.items()
                                            ])
        else:
            self.column_choices = self._column_choices_map = dict()
        if self.column_formatters_export is None:
            self.column_formatters_export = self.column_formatters
        if self.column_type_formatters is None:
            self.column_type_formatters = dict(typefmt.BASE_FORMATTERS)
        if self.column_type_formatters_export is None:
            self.column_type_formatters_export = dict(typefmt.EXPORT_FORMATTERS)
        if self.column_descriptions is None:
            self.column_descriptions = dict()
        self._refresh_filters_cache()
        self._refresh_form_rules_cache()
        self._validate_form_class(self._form_edit_rules, self._edit_form_class)
        self._validate_form_class(self._form_create_rules, self._create_form_class)
        return

    def get_pk_value(self, model):
        """
            Return PK value from a model object.
        """
        raise NotImplementedError()

    def scaffold_list_columns(self):
        """
            Return list of the model field names. Must be implemented in
            the child class.

            Expected return format is list of tuples with field name and
            display text. For example::

                ['name', 'first_name', 'last_name']
        """
        raise NotImplementedError('Please implement scaffold_list_columns method')

    def get_column_name(self, field):
        """
            Return a human-readable column name.

            :param field:
                Model field name.
        """
        if self.column_labels and field in self.column_labels:
            return self.column_labels[field]
        else:
            return self._prettify_name(field)

    def get_list_row_actions(self):
        """
            Return list of row action objects, each is instance of :class:`~flask_admin.model.template.BaseListRowAction`
        """
        actions = []
        if self.can_view_details:
            if self.details_modal:
                actions.append(template.ViewPopupRowAction())
            else:
                actions.append(template.ViewRowAction())
        if self.can_edit:
            if self.edit_modal:
                actions.append(template.EditPopupRowAction())
            else:
                actions.append(template.EditRowAction())
        if self.can_delete:
            actions.append(template.DeleteRowAction())
        return actions + (self.column_extra_row_actions or [])

    def get_column_names(self, only_columns, excluded_columns):
        """
            Returns a list of tuples with the model field name and formatted
            field name.

            :param only_columns:
                List of columns to include in the results. If not set,
                `scaffold_list_columns` will generate the list from the model.
            :param excluded_columns:
                List of columns to exclude from the results if `only_columns`
                is not set.
        """
        if excluded_columns:
            only_columns = [ c for c in only_columns if c not in excluded_columns ]
        return [ (c, self.get_column_name(c)) for c in only_columns ]

    def get_list_columns(self):
        """
            Uses `get_column_names` to get a list of tuples with the model
            field name and formatted name for the columns in `column_list`
            and not in `column_exclude_list`. If `column_list` is not set,
            the columns from `scaffold_list_columns` will be used.
        """
        return self.get_column_names(only_columns=self.column_list or self.scaffold_list_columns(), excluded_columns=self.column_exclude_list)

    def get_details_columns(self):
        """
            Uses `get_column_names` to get a list of tuples with the model
            field name and formatted name for the columns in `column_details_list`
            and not in `column_details_exclude_list`. If `column_details_list`
            is not set, it will attempt to use the columns from `column_list`
            or finally the columns from `scaffold_list_columns` will be used.
        """
        only_columns = self.column_details_list or self.column_list or self.scaffold_list_columns()
        return self.get_column_names(only_columns=only_columns, excluded_columns=self.column_details_exclude_list)

    def get_export_columns(self):
        """
            Uses `get_column_names` to get a list of tuples with the model
            field name and formatted name for the columns in `column_export_list`
            and not in `column_export_exclude_list`. If `column_export_list` is
            not set, it will attempt to use the columns from `column_list`
            or finally the columns from `scaffold_list_columns` will be used.
        """
        only_columns = self.column_export_list or self.column_list or self.scaffold_list_columns()
        return self.get_column_names(only_columns=only_columns, excluded_columns=self.column_export_exclude_list)

    def scaffold_sortable_columns(self):
        """
            Returns dictionary of sortable columns. Must be implemented in
            the child class.

            Expected return format is a dictionary, where keys are field names and
            values are property names.
        """
        raise NotImplementedError('Please implement scaffold_sortable_columns method')

    def get_sortable_columns(self):
        """
            Returns a dictionary of the sortable columns. Key is a model
            field name and value is sort column (for example - attribute).

            If `column_sortable_list` is set, will use it. Otherwise, will call
            `scaffold_sortable_columns` to get them from the model.
        """
        if self.column_sortable_list is None:
            return self.scaffold_sortable_columns() or dict()
        else:
            result = dict()
            for c in self.column_sortable_list:
                if isinstance(c, tuple):
                    result[c[0]] = c[1]
                else:
                    result[c] = c

            return result
            return

    def init_search(self):
        """
            Initialize search. If data provider does not support search,
            `init_search` will return `False`.
        """
        return False

    def scaffold_filters(self, name):
        """
            Generate filter object for the given name

            :param name:
                Name of the field
        """
        return

    def is_valid_filter(self, filter):
        """
            Verify that the provided filter object is valid.

            Override in model backend implementation to verify if
            the provided filter type is allowed.

            :param filter:
                Filter object to verify.
        """
        return isinstance(filter, filters.BaseFilter)

    def handle_filter(self, filter):
        """
            Postprocess (add joins, etc) for a filter.

            :param filter:
                Filter object to postprocess
        """
        return filter

    def get_filters(self):
        """
            Return a list of filter objects.

            If your model backend implementation does not support filters,
            override this method and return `None`.
        """
        if self.column_filters:
            collection = []
            for n in self.column_filters:
                if self.is_valid_filter(n):
                    collection.append(self.handle_filter(n))
                else:
                    flt = self.scaffold_filters(n)
                    if flt:
                        collection.extend(flt)
                    else:
                        raise Exception('Unsupported filter type %s' % n)

            return collection
        return
        return

    def get_filter_arg(self, index, flt):
        """
            Given a filter `flt`, return a unique name for that filter in
            this view.

            Does not include the `flt[n]_` portion of the filter name.

            :param index:
                Filter index in _filters array
            :param flt:
                Filter instance
        """
        if self.named_filter_urls:
            name = ('%s %s' % (flt.name, as_unicode(flt.operation()))).lower()
            name = filter_char_re.sub('', name)
            name = filter_compact_re.sub('_', name)
            return name
        else:
            return str(index)

    def _get_filter_groups(self):
        """
            Returns non-lazy version of filter strings
        """
        if self._filter_groups:
            results = OrderedDict()
            for group in itervalues(self._filter_groups):
                key, items = group.non_lazy()
                results[key] = items

            return results
        return

    def scaffold_form(self):
        """
            Create `form.BaseForm` inherited class from the model. Must be
            implemented in the child class.
        """
        raise NotImplementedError('Please implement scaffold_form method')

    def scaffold_list_form(self, widget=None, validators=None):
        """
            Create form for the `index_view` using only the columns from
            `self.column_editable_list`.

            :param widget:
                WTForms widget class. Defaults to `XEditableWidget`.
            :param validators:
                `form_args` dict with only validators
                {'name': {'validators': [DataRequired()]}}

            Must be implemented in the child class.
        """
        raise NotImplementedError('Please implement scaffold_list_form method')

    def get_form(self):
        """
            Get form class.

            If ``self.form`` is set, will return it and will call
            ``self.scaffold_form`` otherwise.

            Override to implement customized behavior.
        """
        if self.form is not None:
            return self.form
        else:
            return self.scaffold_form()

    def get_list_form(self):
        """
            Get form class for the editable list view.

            Uses only validators from `form_args` to build the form class.

            Allows overriding the editable list view field/widget. For example::

                from flask_admin.model.widgets import XEditableWidget

                class CustomWidget(XEditableWidget):
                    def get_kwargs(self, subfield, kwargs):
                        if subfield.type == 'TextAreaField':
                            kwargs['data-type'] = 'textarea'
                            kwargs['data-rows'] = '20'
                        # elif: kwargs for other fields

                        return kwargs

                class MyModelView(BaseModelView):
                    def get_list_form(self):
                        return self.scaffold_list_form(widget=CustomWidget)
        """
        if self.form_args:
            validators = dict((key, {'validators': value['validators']}) for key, value in iteritems(self.form_args) if value.get('validators'))
        else:
            validators = None
        return self.scaffold_list_form(validators=validators)

    def get_create_form(self):
        """
            Create form class for model creation view.

            Override to implement customized behavior.
        """
        return self.get_form()

    def get_edit_form(self):
        """
            Create form class for model editing view.

            Override to implement customized behavior.
        """
        return self.get_form()

    def get_delete_form(self):
        """
            Create form class for model delete view.

            Override to implement customized behavior.
        """

        class DeleteForm(self.form_base_class):
            id = HiddenField(validators=[InputRequired()])
            url = HiddenField()

        return DeleteForm

    def create_form(self, obj=None):
        """
            Instantiate model creation form and return it.

            Override to implement custom behavior.
        """
        return self._create_form_class(get_form_data(), obj=obj)

    def edit_form(self, obj=None):
        """
            Instantiate model editing form and return it.

            Override to implement custom behavior.
        """
        return self._edit_form_class(get_form_data(), obj=obj)

    def delete_form(self):
        """
            Instantiate model delete form and return it.

            Override to implement custom behavior.

            The delete form originally used a GET request, so delete_form
            accepts both GET and POST request for backwards compatibility.
        """
        if request.form:
            return self._delete_form_class(request.form)
        else:
            if request.args:
                return self._delete_form_class(request.args)
            return self._delete_form_class()

    def list_form(self, obj=None):
        """
            Instantiate model editing form for list view and return it.

            Override to implement custom behavior.
        """
        return self._list_form_class(get_form_data(), obj=obj)

    def validate_form(self, form):
        """
            Validate the form on submit.

            :param form:
                Form to validate
        """
        return validate_form_on_submit(form)

    def get_save_return_url(self, model, is_created=False):
        """
            Return url where user is redirected after successful form save.

            :param model:
                Saved object
            :param is_created:
                Whether new object was created or existing one was updated

            For example, redirect use to object details view after form save::

                class MyModelView(ModelView):
                    can_view_details = True

                    def get_save_return_url(self, model, is_created):
                        return self.get_url('.details_view', id=model.id)

        """
        return get_redirect_target() or self.get_url('.index_view')

    def _get_ruleset_missing_fields(self, ruleset, form):
        missing_fields = []
        if ruleset:
            visible_fields = ruleset.visible_fields
            for field in form:
                if field.name not in visible_fields:
                    missing_fields.append(field.name)

        return missing_fields

    def _show_missing_fields_warning(self, text):
        warnings.warn(text)

    def _validate_form_class(self, ruleset, form_class, remove_missing=True):
        form_fields = []
        for name, obj in iteritems(form_class.__dict__):
            if isinstance(obj, UnboundField):
                form_fields.append(name)

        missing_fields = []
        if ruleset:
            visible_fields = ruleset.visible_fields
            for field_name in form_fields:
                if field_name not in visible_fields:
                    missing_fields.append(field_name)

        if missing_fields:
            self._show_missing_fields_warning('Fields missing from ruleset: %s' % (',').join(missing_fields))
        if remove_missing:
            self._remove_fields_from_form_class(missing_fields, form_class)

    def _validate_form_instance(self, ruleset, form, remove_missing=True):
        missing_fields = self._get_ruleset_missing_fields(ruleset=ruleset, form=form)
        if missing_fields:
            self._show_missing_fields_warning('Fields missing from ruleset: %s' % (',').join(missing_fields))
        if remove_missing:
            self._remove_fields_from_form_instance(missing_fields, form)

    def _remove_fields_from_form_instance(self, field_names, form):
        for field_name in field_names:
            form.__delitem__(field_name)

    def _remove_fields_from_form_class(self, field_names, form_class):
        for field_name in field_names:
            delattr(form_class, field_name)

    def is_sortable(self, name):
        """
            Verify if column is sortable.

            Not case-sensitive.

            :param name:
                Column name.
        """
        return name.lower() in (x.lower() for x in self._sortable_columns)

    def is_editable(self, name):
        """
            Verify if column is editable.

            :param name:
                Column name.
        """
        return name in self.column_editable_list

    def _get_column_by_idx(self, idx):
        """
            Return column index by
        """
        if idx is None or idx < 0 or idx >= len(self._list_columns):
            return
        return self._list_columns[idx]

    def _get_default_order(self):
        """
            Return default sort order
        """
        if self.column_default_sort:
            if isinstance(self.column_default_sort, tuple):
                return self.column_default_sort
            else:
                return (
                 self.column_default_sort, False)

        return

    def get_list(self, page, sort_field, sort_desc, search, filters, page_size=None):
        """
            Return a paginated and sorted list of models from the data source.

            Must be implemented in the child class.

            :param page:
                Page number, 0 based. Can be set to None if it is first page.
            :param sort_field:
                Sort column name or None.
            :param sort_desc:
                If set to True, sorting is in descending order.
            :param search:
                Search query
            :param filters:
                List of filter tuples. First value in a tuple is a search
                index, second value is a search value.
            :param page_size:
                Number of results. Defaults to ModelView's page_size. Can be
                overriden to change the page_size limit. Removing the page_size
                limit requires setting page_size to 0 or False.
        """
        raise NotImplementedError('Please implement get_list method')

    def get_one(self, id):
        """
            Return one model by its id.

            Must be implemented in the child class.

            :param id:
                Model id
        """
        raise NotImplementedError('Please implement get_one method')

    def handle_view_exception(self, exc):
        if isinstance(exc, ValidationError):
            flash(as_unicode(exc), 'error')
            return True
        if current_app.config.get('ADMIN_RAISE_ON_VIEW_EXCEPTION'):
            raise
        if self._debug:
            raise
        return False

    def on_model_change(self, form, model, is_created):
        """
            Perform some actions before a model is created or updated.

            Called from create_model and update_model in the same transaction
            (if it has any meaning for a store backend).

            By default does nothing.

            :param form:
                Form used to create/update model
            :param model:
                Model that will be created/updated
            :param is_created:
                Will be set to True if model was created and to False if edited
        """
        pass

    def _on_model_change(self, form, model, is_created):
        """
            Compatibility helper.
        """
        try:
            self.on_model_change(form, model, is_created)
        except TypeError:
            msg = ('%s.on_model_change() now accepts third ' + 'parameter is_created. Please update your code') % self.model
            warnings.warn(msg)
            self.on_model_change(form, model)

    def after_model_change(self, form, model, is_created):
        """
            Perform some actions after a model was created or updated and
            committed to the database.

            Called from create_model after successful database commit.

            By default does nothing.

            :param form:
                Form used to create/update model
            :param model:
                Model that was created/updated
            :param is_created:
                True if model was created, False if model was updated
        """
        pass

    def on_model_delete(self, model):
        """
            Perform some actions before a model is deleted.

            Called from delete_model in the same transaction
            (if it has any meaning for a store backend).

            By default do nothing.
        """
        pass

    def after_model_delete(self, model):
        """
            Perform some actions after a model was deleted and
            committed to the database.

            Called from delete_model after successful database commit
            (if it has any meaning for a store backend).

            By default does nothing.

            :param model:
                Model that was deleted
        """
        pass

    def on_form_prefill(self, form, id):
        """
            Perform additional actions to pre-fill the edit form.

            Called from edit_view, if the current action is rendering
            the form rather than receiving client side input, after
            default pre-filling has been performed.

            By default does nothing.

            You only need to override this if you have added custom
            fields that depend on the database contents in a way that
            Flask-admin can't figure out by itself. Fields that were
            added by name of a normal column or relationship should
            work out of the box.

            :param form:
                Form instance
            :param id:
                id of the object that is going to be edited
        """
        pass

    def create_model(self, form):
        """
            Create model from the form.

            Returns the model instance if operation succeeded.

            Must be implemented in the child class.

            :param form:
                Form instance
        """
        raise NotImplementedError()

    def update_model(self, form, model):
        """
            Update model from the form.

            Returns `True` if operation succeeded.

            Must be implemented in the child class.

            :param form:
                Form instance
            :param model:
                Model instance
        """
        raise NotImplementedError()

    def delete_model(self, model):
        """
            Delete model.

            Returns `True` if operation succeeded.

            Must be implemented in the child class.

            :param model:
                Model instance
        """
        raise NotImplementedError()

    def _prettify_name(self, name):
        """
            Prettify pythonic variable name.

            For example, 'hello_world' will be converted to 'Hello World'

            :param name:
                Name to prettify
        """
        return prettify_name(name)

    def get_empty_list_message(self):
        return gettext('There are no items in the table.')

    def _get_list_filter_args(self):
        if self._filters:
            filters = []
            for n in request.args:
                if not n.startswith('flt'):
                    continue
                if '_' not in n:
                    continue
                pos, key = n[3:].split('_', 1)
                if key in self._filter_args:
                    idx, flt = self._filter_args[key]
                    value = request.args[n]
                    if flt.validate(value):
                        filters.append((pos, (idx, as_unicode(flt.name), value)))
                    else:
                        flash(gettext('Invalid Filter Value: %(value)s', value=value), 'error')

            return [ v[1] for v in sorted(filters, key=lambda n: n[0]) ]
        else:
            return

    def _get_list_extra_args(self):
        """
            Return arguments from query string.
        """
        return ViewArgs(page=request.args.get('page', 0, type=int), sort=request.args.get('sort', None, type=int), sort_desc=request.args.get('desc', None, type=int), search=request.args.get('search', None), filters=self._get_list_filter_args())

    def _get_list_url(self, view_args):
        """
            Generate page URL with current page, sort column and
            other parameters.

            :param view:
                View name
            :param view_args:
                ViewArgs object with page number, filters, etc.
        """
        page = view_args.page or None
        desc = 1 if view_args.sort_desc else None
        kwargs = dict(page=page, sort=view_args.sort, desc=desc, search=view_args.search)
        kwargs.update(view_args.extra_args)
        if view_args.filters:
            for i, pair in enumerate(view_args.filters):
                idx, flt_name, value = pair
                key = 'flt%d_%s' % (i, self.get_filter_arg(idx, self._filters[idx]))
                kwargs[key] = value

        return self.get_url('.index_view', **kwargs)

    def is_action_allowed(self, name):
        """
            Override this method to allow or disallow actions based
            on some condition.

            The default implementation only checks if the particular action
            is not in `action_disallowed_list`.
        """
        return name not in self.action_disallowed_list

    def _get_field_value(self, model, name):
        """
            Get unformatted field value from the model
        """
        return rec_getattr(model, name)

    def _get_list_value(self, context, model, name, column_formatters, column_type_formatters):
        """
            Returns the value to be displayed.

            :param context:
                :py:class:`jinja2.runtime.Context` if available
            :param model:
                Model instance
            :param name:
                Field name
            :param column_formatters:
                column_formatters to be used.
            :param column_type_formatters:
                column_type_formatters to be used.
        """
        column_fmt = column_formatters.get(name)
        if column_fmt is not None:
            value = column_fmt(self, context, model, name)
        else:
            value = self._get_field_value(model, name)
        choices_map = self._column_choices_map.get(name, {})
        if choices_map:
            return choices_map.get(value) or value
        else:
            type_fmt = None
            for typeobj, formatter in column_type_formatters.items():
                if isinstance(value, typeobj):
                    type_fmt = formatter
                    break

            if type_fmt is not None:
                value = type_fmt(self, value)
            return value

    @contextfunction
    def get_list_value(self, context, model, name):
        """
            Returns the value to be displayed in the list view

            :param context:
                :py:class:`jinja2.runtime.Context`
            :param model:
                Model instance
            :param name:
                Field name
        """
        return self._get_list_value(context, model, name, self.column_formatters, self.column_type_formatters)

    def get_export_value(self, model, name):
        """
            Returns the value to be displayed in export.
            Allows export to use different (non HTML) formatters.

            :param model:
                Model instance
            :param name:
                Field name
        """
        return self._get_list_value(None, model, name, self.column_formatters_export, self.column_type_formatters_export)

    def get_export_name(self, export_type='csv'):
        """
        :return: The exported csv file name.
        """
        filename = '%s_%s.%s' % (self.name,
         time.strftime('%Y-%m-%d_%H-%M-%S'),
         export_type)
        return filename

    def _process_ajax_references(self):
        """
            Process `form_ajax_refs` and generate model loaders that
            will be used by the `ajax_lookup` view.
        """
        result = {}
        if self.form_ajax_refs:
            for name, options in iteritems(self.form_ajax_refs):
                if isinstance(options, dict):
                    result[name] = self._create_ajax_loader(name, options)
                elif isinstance(options, AjaxModelLoader):
                    result[name] = options
                else:
                    raise ValueError('%s.form_ajax_refs can not handle %s types' % (self, type(options)))

        return result

    def _create_ajax_loader(self, name, options):
        """
            Model backend will override this to implement AJAX model loading.
        """
        raise NotImplementedError()

    @expose('/')
    def index_view(self):
        """
            List view
        """
        if self.can_delete:
            delete_form = self.delete_form()
        else:
            delete_form = None
        view_args = self._get_list_extra_args()
        sort_column = self._get_column_by_idx(view_args.sort)
        if sort_column is not None:
            sort_column = sort_column[0]
        count, data = self.get_list(view_args.page, sort_column, view_args.sort_desc, view_args.search, view_args.filters)
        list_forms = {}
        if self.column_editable_list:
            for row in data:
                list_forms[self.get_pk_value(row)] = self.list_form(obj=row)

        if count is not None and self.page_size:
            num_pages = int(ceil(count / float(self.page_size)))
        elif not self.page_size:
            num_pages = 0
        else:
            num_pages = None

        def pager_url(p):
            if p == 0:
                p = None
            return self._get_list_url(view_args.clone(page=p))

        def sort_url(column, invert=False):
            desc = None
            if invert and not view_args.sort_desc:
                desc = 1
            return self._get_list_url(view_args.clone(sort=column, sort_desc=desc))

        actions, actions_confirmation = self.get_actions_list()
        clear_search_url = self._get_list_url(view_args.clone(page=0, sort=view_args.sort, sort_desc=view_args.sort_desc, search=None, filters=None))
        return self.render(self.list_template, data=data, list_forms=list_forms, delete_form=delete_form, list_columns=self._list_columns, sortable_columns=self._sortable_columns, editable_columns=self.column_editable_list, list_row_actions=self.get_list_row_actions(), count=count, pager_url=pager_url, num_pages=num_pages, page=view_args.page, page_size=self.page_size, sort_column=view_args.sort, sort_desc=view_args.sort_desc, sort_url=sort_url, search_supported=self._search_supported, clear_search_url=clear_search_url, search=view_args.search, filters=self._filters, filter_groups=self._get_filter_groups(), active_filters=view_args.filters, actions=actions, actions_confirmation=actions_confirmation, enumerate=enumerate, get_pk_value=self.get_pk_value, get_value=self.get_list_value, return_url=self._get_list_url(view_args))

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        """
            Create model view
        """
        return_url = get_redirect_target() or self.get_url('.index_view')
        if not self.can_create:
            return redirect(return_url)
        form = self.create_form()
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_create_rules, form=form)
        if self.validate_form(form):
            model = self.create_model(form)
            if model:
                flash(gettext('Record was successfully created.'), 'success')
                if '_add_another' in request.form:
                    return redirect(request.url)
                if '_continue_editing' in request.form:
                    if model is not True:
                        url = self.get_url('.edit_view', id=self.get_pk_value(model), url=return_url)
                    else:
                        url = return_url
                    return redirect(url)
                return redirect(self.get_save_return_url(model, is_created=True))
        form_opts = FormOpts(widget_args=self.form_widget_args, form_rules=self._form_create_rules)
        if self.create_modal and request.args.get('modal'):
            template = self.create_modal_template
        else:
            template = self.create_template
        return self.render(template, form=form, form_opts=form_opts, return_url=return_url)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        """
            Edit model view
        """
        return_url = get_redirect_target() or self.get_url('.index_view')
        if not self.can_edit:
            return redirect(return_url)
        else:
            id = get_mdict_item_or_list(request.args, 'id')
            if id is None:
                return redirect(return_url)
            model = self.get_one(id)
            if model is None:
                flash(gettext('Record does not exist.'), 'error')
                return redirect(return_url)
            form = self.edit_form(obj=model)
            if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
                self._validate_form_instance(ruleset=self._form_edit_rules, form=form)
            if self.validate_form(form):
                if self.update_model(form, model):
                    flash(gettext('Record was successfully saved.'), 'success')
                    if '_add_another' in request.form:
                        return redirect(self.get_url('.create_view', url=return_url))
                    if '_continue_editing' in request.form:
                        return redirect(request.url)
                    return redirect(self.get_save_return_url(model, is_created=False))
            if request.method == 'GET':
                self.on_form_prefill(form, id)
            form_opts = FormOpts(widget_args=self.form_widget_args, form_rules=self._form_edit_rules)
            if self.edit_modal and request.args.get('modal'):
                template = self.edit_modal_template
            else:
                template = self.edit_template
            return self.render(template, model=model, form=form, form_opts=form_opts, return_url=return_url)

    @expose('/details/')
    def details_view(self):
        """
            Details model view
        """
        return_url = get_redirect_target() or self.get_url('.index_view')
        if not self.can_view_details:
            return redirect(return_url)
        else:
            id = get_mdict_item_or_list(request.args, 'id')
            if id is None:
                return redirect(return_url)
            model = self.get_one(id)
            if model is None:
                flash(gettext('Record does not exist.'), 'error')
                return redirect(return_url)
            if self.details_modal and request.args.get('modal'):
                template = self.details_modal_template
            else:
                template = self.details_template
            return self.render(template, model=model, details_columns=self._details_columns, get_value=self.get_list_value, return_url=return_url)

    @expose('/delete/', methods=('POST', ))
    def delete_view(self):
        """
            Delete model view. Only POST method is allowed.
        """
        return_url = get_redirect_target() or self.get_url('.index_view')
        if not self.can_delete:
            return redirect(return_url)
        else:
            form = self.delete_form()
            if self.validate_form(form):
                id = form.id.data
                model = self.get_one(id)
                if model is None:
                    flash(gettext('Record does not exist.'), 'error')
                    return redirect(return_url)
                if self.delete_model(model):
                    flash(gettext('Record was successfully deleted.'), 'success')
                    return redirect(return_url)
            else:
                flash_errors(form, message='Failed to delete record. %(error)s')
            return redirect(return_url)

    @expose('/action/', methods=('POST', ))
    def action_view(self):
        """
            Mass-model action view.
        """
        return self.handle_action()

    def _export_data(self):
        for col, func in iteritems(self.column_formatters_export):
            if col not in [ col for col, _ in self._export_columns ]:
                continue
            if func.__name__ == 'inner':
                raise NotImplementedError('Macros are not implemented in export. Exclude column in column_formatters_export, column_export_list, or  column_export_exclude_list. Column: %s' % (
                 col,))

        view_args = self._get_list_extra_args()
        sort_column = self._get_column_by_idx(view_args.sort)
        if sort_column is not None:
            sort_column = sort_column[0]
        count, data = self.get_list(0, sort_column, view_args.sort_desc, view_args.search, view_args.filters, page_size=self.export_max_rows)
        return (
         count, data)

    @expose('/export/<export_type>/')
    def export(self, export_type):
        return_url = get_redirect_target() or self.get_url('.index_view')
        if not self.can_export or export_type not in self.export_types:
            flash(gettext('Permission denied.'), 'error')
            return redirect(return_url)
        else:
            if export_type == 'csv':
                return self._export_csv(return_url)
            return self._export_tablib(export_type, return_url)

    def _export_csv(self, return_url):
        """
            Export a CSV of records as a stream.
        """
        count, data = self._export_data()

        class Echo(object):
            """
            An object that implements just the write method of the file-like
            interface.
            """

            def write(self, value):
                """
                Write the value by returning it, instead of storing
                in a buffer.
                """
                return value

        writer = csv.writer(Echo())

        def generate():
            titles = [ csv_encode(c[1]) for c in self._export_columns ]
            yield writer.writerow(titles)
            for row in data:
                vals = [ csv_encode(self.get_export_value(row, c[0])) for c in self._export_columns
                       ]
                yield writer.writerow(vals)

        filename = self.get_export_name(export_type='csv')
        disposition = 'attachment;filename=%s' % (secure_filename(filename),)
        return Response(stream_with_context(generate()), headers={'Content-Disposition': disposition}, mimetype='text/csv')

    def _export_tablib(self, export_type, return_url):
        """
            Exports a variety of formats using the tablib library.
        """
        if tablib is None:
            flash(gettext('Tablib dependency not installed.'), 'error')
            return redirect(return_url)
        else:
            filename = self.get_export_name(export_type)
            disposition = 'attachment;filename=%s' % (secure_filename(filename),)
            mimetype, encoding = mimetypes.guess_type(filename)
            if not mimetype:
                mimetype = 'application/octet-stream'
            if encoding:
                mimetype = '%s; charset=%s' % (mimetype, encoding)
            ds = tablib.Dataset(headers=[ c[1] for c in self._export_columns ])
            count, data = self._export_data()
            for row in data:
                vals = [ self.get_export_value(row, c[0]) for c in self._export_columns ]
                ds.append(vals)

            try:
                try:
                    response_data = ds.export(format=export_type)
                except AttributeError:
                    response_data = getattr(ds, export_type)

            except (AttributeError, tablib.UnsupportedFormat):
                flash(gettext('Export type "%(type)s not supported.', type=export_type), 'error')
                return redirect(return_url)

            return Response(response_data, headers={'Content-Disposition': disposition}, mimetype=mimetype)

    @expose('/ajax/lookup/')
    def ajax_lookup(self):
        name = request.args.get('name')
        query = request.args.get('query')
        offset = request.args.get('offset', type=int)
        limit = request.args.get('limit', 10, type=int)
        loader = self._form_ajax_refs.get(name)
        if not loader:
            abort(404)
        data = [ loader.format(m) for m in loader.get_list(query, offset, limit) ]
        return Response(json.dumps(data), mimetype='application/json')

    @expose('/ajax/update/', methods=('POST', ))
    def ajax_update(self):
        """
            Edits a single column of a record in list view.
        """
        if not self.column_editable_list:
            abort(404)
        form = self.list_form()
        for field in list(form):
            if field.name in request.form or field.name == 'csrf_token':
                pass
            else:
                form.__delitem__(field.name)

        if self.validate_form(form):
            pk = form.list_form_pk.data
            record = self.get_one(pk)
            if record is None:
                return (gettext('Record does not exist.'), 500)
            if self.update_model(form, record):
                return gettext('Record was successfully saved.')
            msgs = (', ').join([ msg for msg in get_flashed_messages() ])
            return (
             gettext('Failed to update record. %(error)s', error=msgs), 500)
        else:
            for field in form:
                for error in field.errors:
                    if isinstance(error, list):
                        return (
                         gettext('Failed to update record. %(error)s', error=(', ').join(error)), 500)
                    else:
                        return (
                         gettext('Failed to update record. %(error)s', error=error), 500)

        return