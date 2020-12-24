# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\opt\private\cw1427\fab-admin\fab_admin\fab_manager_overwrite\flask_appbuilder/baseviews.py
# Compiled at: 2020-02-04 09:36:17
# Size of source mod 2**32: 44197 bytes
from inspect import isclass
import json, logging
from datetime import datetime, date
from flask import Blueprint, session, flash, render_template, url_for, abort
from flask_appbuilder._compat import as_unicode
from flask_appbuilder.forms import GeneralModelConverter
from flask_appbuilder.widgets import FormWidget, ShowWidget, ListWidget, SearchWidget
from flask_appbuilder.actions import ActionItem
from flask_appbuilder.urltools import *
log = logging.getLogger(__name__)

def expose(url='/', methods=('GET',)):
    """
        Use this decorator to expose views on your view classes.
        :param url:
            Relative URL for the view
        :param methods:
            Allowed HTTP methods. By default only GET is allowed.
    """

    def wrap(f):
        if not hasattr(f, '_urls'):
            f._urls = []
        f._urls.append((url, methods))
        return f

    return wrap


def expose_api(name='', url='', methods=('GET',), description=''):

    def wrap(f):
        api_name = name or f.__name__
        api_url = url or '/api/{0}'.format(name)
        if not hasattr(f, '_urls'):
            f._urls = []
            f._extra = {}
        f._urls.append((api_url, methods))
        f._extra[api_name] = (api_url, f.__name__, description)
        return f

    return wrap


class BaseView(object):
    __doc__ = "\n        All views inherit from this class.\n        it's constructor will register your exposed urls on flask as a Blueprint.\n        This class does not expose any urls, but provides a common base for all views.\n        Extend this class if you want to expose methods for your own templates\n    "
    appbuilder = None
    blueprint = None
    endpoint = None
    route_base = None
    template_folder = 'templates'
    static_folder = 'static'
    static_url_path = '/static'
    base_permissions = None
    base_permissions_inclusive = ['menu_access']
    default_view = 'list'
    extra_args = None
    _apis = None

    def __init__(self):
        """
            Initialization of base permissions
            based on exposed methods and actions
            Initialization of extra args
        """
        if self.base_permissions is None:
            self.base_permissions = set()
            for attr_name in dir(self):
                if hasattr(getattr(self, attr_name), '_permission_name'):
                    permission_name = getattr(getattr(self, attr_name), '_permission_name')
                    self.base_permissions.add('can_' + permission_name)

            self.base_permissions = list(self.base_permissions)
        else:
            if self.base_permissions_inclusive:
                self.base_permissions.extend(self.base_permissions_inclusive)
            self.extra_args = self.extra_args or dict()
        self._apis = dict()
        for attr_name in dir(self):
            if hasattr(getattr(self, attr_name), '_extra'):
                _extra = getattr(getattr(self, attr_name), '_extra')
                for key in _extra:
                    self._apis[key] = _extra[key]

    def create_blueprint(self, appbuilder, endpoint=None, static_folder=None, static_url_path=None):
        """
            Create Flask blueprint. You will generally not use it
            :param appbuilder:
               the AppBuilder object
            :param endpoint:
               endpoint override for this blueprint, will assume class name if not provided
            :param static_folder:
               the relative override for static folder, if omitted application will use the appbuilder static
        """
        self.appbuilder = appbuilder
        self.endpoint = endpoint or self.__class__.__name__
        if self.route_base is None:
            self.route_base = '/' + self.__class__.__name__.lower()
        else:
            if static_url_path:
                self.static_url_path = static_url_path
            if not static_folder:
                self.blueprint = Blueprint((self.endpoint), (self.__module__), url_prefix=(self.route_base),
                  template_folder=(self.template_folder),
                  static_folder=(self.static_folder),
                  static_url_path=(self.static_url_path))
            else:
                self.blueprint = Blueprint((self.endpoint), (self.__module__), url_prefix=(self.route_base),
                  template_folder=(self.template_folder),
                  static_folder=static_folder,
                  static_url_path=(self.static_url_path))
        self._register_urls()
        return self.blueprint

    def _register_urls(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, '_urls'):
                for url, methods in attr._urls:
                    self.blueprint.add_url_rule(url, attr_name,
                      attr,
                      methods=methods)

    def render_template(self, template, **kwargs):
        """
            Use this method on your own endpoints, will pass the extra_args
            to the templates.
            :param template: The template relative path
            :param kwargs: arguments to be passed to the template
        """
        kwargs['base_template'] = self.appbuilder.base_template
        kwargs['appbuilder'] = self.appbuilder
        return render_template(template, **dict(list(kwargs.items()) + list(self.extra_args.items())))

    def _prettify_name(self, name):
        """
            Prettify pythonic variable name.
            For example, 'HelloWorld' will be converted to 'Hello World'
            :param name:
                Name to prettify.
        """
        return re.sub('(?<=.)([A-Z])', ' \\1', name)

    def _prettify_column(self, name):
        """
            Prettify pythonic variable name.
            For example, 'hello_world' will be converted to 'Hello World'
            :param name:
                Name to prettify.
        """
        return re.sub('[._]', ' ', name).title()

    def update_redirect(self):
        """
            Call it on your own endpoint's to update the back history navigation.
            If you bypass it, the next submit or back will go over it.
        """
        page_history = Stack(session.get('page_history', []))
        page_history.push(request.url)
        session['page_history'] = page_history.to_json()

    def get_redirect(self):
        """
            Returns the previous url.
        """
        index_url = self.appbuilder.get_url_for_index
        page_history = Stack(session.get('page_history', []))
        if page_history.pop() is None:
            return index_url
        else:
            session['page_history'] = page_history.to_json()
            url = page_history.pop() or index_url
            return url

    @classmethod
    def get_default_url(cls, **kwargs):
        """
            Returns the url for this class default endpoint
        """
        return url_for((cls.__name__ + '.' + cls.default_view), **kwargs)

    def get_uninit_inner_views(self):
        """
            Will return a list with views that need to be initialized.
            Normally related_views from ModelView
        """
        return []

    def get_init_inner_views(self, views):
        """
            Sets initialized inner views
        """
        pass


class BaseFormView(BaseView):
    __doc__ = "\n        Base class FormView's\n    "
    form_template = 'appbuilder/general/model/edit.html'
    edit_widget = FormWidget
    form_title = ''
    form_columns = None
    form = None
    form_fieldsets = None
    default_view = 'this_form_get'

    def _init_vars(self):
        self.form_columns = self.form_columns or []
        self.form_fieldsets = self.form_fieldsets or []
        list_cols = [field.name for field in self.form.refresh()]
        if self.form_fieldsets:
            self.form_columns = []
            for fieldset_item in self.form_fieldsets:
                self.form_columns = self.form_columns + list(fieldset_item[1].get('fields'))

        elif not self.form_columns:
            self.form_columns = list_cols

    def form_get(self, form):
        """
            Override this method to implement your form processing
        """
        pass

    def form_post(self, form):
        """
            Override this method to implement your form processing
            :param form: WTForm form
            Return None or a flask response to render
            a custom template or redirect the user
        """
        pass

    def _get_edit_widget(self, form=None, exclude_cols=None, widgets=None):
        exclude_cols = exclude_cols or []
        widgets = widgets or {}
        widgets['edit'] = self.edit_widget(route_base=(self.route_base), form=form,
          include_cols=(self.form_columns),
          exclude_cols=exclude_cols,
          fieldsets=(self.form_fieldsets))
        return widgets


class BaseModelView(BaseView):
    __doc__ = '\n        The base class of ModelView and ChartView, all properties are inherited\n        Customize ModelView and ChartView overriding this properties\n        This class supports all the basics for query\n    '
    datamodel = None
    title = 'Title'
    search_columns = None
    search_exclude_columns = None
    search_form_extra_fields = None
    search_form_query_rel_fields = None
    label_columns = None
    search_form = None
    base_filters = None
    base_order = None
    search_widget = SearchWidget
    _base_filters = None
    _filters = None

    def __init__(self, **kwargs):
        datamodel = kwargs.get('datamodel', None)
        if datamodel:
            self.datamodel = datamodel
        self._init_properties()
        self._init_forms()
        self._init_titles()
        (super(BaseModelView, self).__init__)(**kwargs)

    def _gen_labels_columns(self, list_columns):
        """
            Auto generates pretty label_columns from list of columns
        """
        for col in list_columns:
            if not self.label_columns.get(col):
                self.label_columns[col] = self._prettify_column(col)

    def _init_titles(self):
        pass

    def _init_properties(self):
        self.label_columns = self.label_columns or {}
        self.base_filters = self.base_filters or []
        self.search_exclude_columns = self.search_exclude_columns or []
        self.search_columns = self.search_columns or []
        self._base_filters = self.datamodel.get_filters().add_filter_list(self.base_filters)
        list_cols = self.datamodel.get_columns_list()
        search_columns = self.datamodel.get_search_columns_list()
        if not self.search_columns:
            self.search_columns = [x for x in search_columns if x not in self.search_exclude_columns]
        self._gen_labels_columns(list_cols)
        self._filters = self.datamodel.get_filters(self.search_columns)

    def _init_forms(self):
        conv = GeneralModelConverter(self.datamodel)
        if not self.search_form:
            self.search_form = conv.create_form((self.label_columns), (self.search_columns),
              extra_fields=(self.search_form_extra_fields),
              filter_rel_fields=(self.search_form_query_rel_fields))

    def _get_search_widget(self, form=None, exclude_cols=None, widgets=None):
        exclude_cols = exclude_cols or []
        widgets = widgets or {}
        widgets['search'] = self.search_widget(route_base=(self.route_base), form=form,
          include_cols=(self.search_columns),
          exclude_cols=exclude_cols,
          filters=(self._filters))
        return widgets

    def _label_columns_json(self):
        """
            Prepares dict with labels to be JSON serializable
        """
        ret = {}
        for key, value in list(self.label_columns.items()):
            ret[key] = as_unicode(value.encode('UTF-8'))

        return ret


class BaseCRUDView(BaseModelView):
    __doc__ = '\n        The base class for ModelView, all properties are inherited\n        Customize ModelView overriding this properties\n    '
    related_views = None
    _related_views = None
    list_title = ''
    show_title = ''
    add_title = ''
    edit_title = ''
    list_columns = None
    show_columns = None
    add_columns = None
    edit_columns = None
    show_exclude_columns = None
    add_exclude_columns = None
    edit_exclude_columns = None
    order_columns = None
    page_size = 10
    show_fieldsets = None
    add_fieldsets = None
    edit_fieldsets = None
    description_columns = None
    validators_columns = None
    formatters_columns = None
    add_form_extra_fields = None
    edit_form_extra_fields = None
    add_form_query_rel_fields = None
    edit_form_query_rel_fields = None
    add_form = None
    edit_form = None
    list_template = 'appbuilder/general/model/list.html'
    edit_template = 'appbuilder/general/model/edit.html'
    add_template = 'appbuilder/general/model/add.html'
    show_template = 'appbuilder/general/model/show.html'
    list_widget = ListWidget
    edit_widget = FormWidget
    add_widget = FormWidget
    show_widget = ShowWidget
    actions = None

    def __init__(self, **kwargs):
        (super(BaseCRUDView, self).__init__)(**kwargs)
        self.actions = {}
        for attr_name in dir(self):
            func = getattr(self, attr_name)
            if hasattr(func, '_action'):
                action = ActionItem(*func._action, **{'func': func})
                self.base_permissions.append(action.name)
                self.actions[action.name] = action

    def _init_forms(self):
        super(BaseCRUDView, self)._init_forms()
        conv = GeneralModelConverter(self.datamodel)
        if not self.add_form:
            self.add_form = conv.create_form(self.label_columns, self.add_columns, self.description_columns, self.validators_columns, self.add_form_extra_fields, self.add_form_query_rel_fields)
        if not self.edit_form:
            self.edit_form = conv.create_form(self.label_columns, self.edit_columns, self.description_columns, self.validators_columns, self.edit_form_extra_fields, self.edit_form_query_rel_fields)

    def _init_titles(self):
        super(BaseCRUDView, self)._init_titles()
        class_name = self.datamodel.model_name
        if not self.list_title:
            self.list_title = 'List ' + self._prettify_name(class_name)
        if not self.add_title:
            self.add_title = 'Add ' + self._prettify_name(class_name)
        if not self.edit_title:
            self.edit_title = 'Edit ' + self._prettify_name(class_name)
        if not self.show_title:
            self.show_title = 'Show ' + self._prettify_name(class_name)
        self.title = self.list_title

    def _init_properties(self):
        super(BaseCRUDView, self)._init_properties()
        self.related_views = self.related_views or []
        self._related_views = self._related_views or []
        self.description_columns = self.description_columns or {}
        self.validators_columns = self.validators_columns or {}
        self.formatters_columns = self.formatters_columns or {}
        self.add_form_extra_fields = self.add_form_extra_fields or {}
        self.edit_form_extra_fields = self.edit_form_extra_fields or {}
        self.show_exclude_columns = self.show_exclude_columns or []
        self.add_exclude_columns = self.add_exclude_columns or []
        self.edit_exclude_columns = self.edit_exclude_columns or []
        list_cols = self.datamodel.get_user_columns_list()
        self.list_columns = self.list_columns or [list_cols[0]]
        self._gen_labels_columns(self.list_columns)
        self.order_columns = self.order_columns or self.datamodel.get_order_columns_list(list_columns=(self.list_columns))
        if self.show_fieldsets:
            self.show_columns = []
            for fieldset_item in self.show_fieldsets:
                self.show_columns = self.show_columns + list(fieldset_item[1].get('fields'))

        else:
            if not self.show_columns:
                self.show_columns = [x for x in list_cols if x not in self.show_exclude_columns]
        if self.add_fieldsets:
            self.add_columns = []
            for fieldset_item in self.add_fieldsets:
                self.add_columns = self.add_columns + list(fieldset_item[1].get('fields'))

        else:
            if not self.add_columns:
                self.add_columns = [x for x in list_cols if x not in self.add_exclude_columns]
            if self.edit_fieldsets:
                self.edit_columns = []
                for fieldset_item in self.edit_fieldsets:
                    self.edit_columns = self.edit_columns + list(fieldset_item[1].get('fields'))

            elif not self.edit_columns:
                self.edit_columns = [x for x in list_cols if x not in self.edit_exclude_columns]

    def _get_related_view_widget(self, item, related_view, order_column='', order_direction='', page=None, page_size=None):
        fk = related_view.datamodel.get_related_fk(self.datamodel.obj)
        filters = related_view.datamodel.get_filters()
        if related_view.datamodel.is_relation_many_to_one(fk):
            filters.add_filter_related_view(fk, self.datamodel.FilterRelationOneToManyEqual, self.datamodel.get_pk_value(item))
        else:
            if related_view.datamodel.is_relation_many_to_many(fk):
                filters.add_filter_related_view(fk, self.datamodel.FilterRelationManyToManyEqual, self.datamodel.get_pk_value(item))
            else:
                if isclass(related_view):
                    if issubclass(related_view, BaseView):
                        name = related_view.__name__
                else:
                    name = related_view.__class__.__name__
                log.error("Can't find relation on related view {0}".format(name))
                return
        return related_view._get_view_widget(filters=filters, order_column=order_column,
          order_direction=order_direction,
          page=page,
          page_size=page_size)

    def _get_related_views_widgets(self, item, orders=None, pages=None, page_sizes=None, widgets=None, **args):
        """
            :return:
                Returns a dict with 'related_views' key with a list of
                Model View widgets
        """
        widgets = widgets or {}
        widgets['related_views'] = []
        for view in self._related_views:
            if orders.get(view.__class__.__name__):
                order_column, order_direction = orders.get(view.__class__.__name__)
            else:
                order_column, order_direction = ('', '')
            widgets['related_views'].append(self._get_related_view_widget(item, view, order_column,
              order_direction, page=(pages.get(view.__class__.__name__)),
              page_size=(page_sizes.get(view.__class__.__name__))))

        return widgets

    def _get_view_widget(self, **kwargs):
        """
            :return:
                Returns a Model View widget
        """
        return (self._get_list_widget)(**kwargs).get('list')

    def _get_list_widget(self, filters, actions=None, order_column='', order_direction='', page=None, page_size=None, widgets=None, **args):
        """ get joined base filter and current active filter for query """
        widgets = widgets or {}
        actions = actions or self.actions
        page_size = page_size or self.page_size
        if not order_column:
            if self.base_order:
                order_column, order_direction = self.base_order
        joined_filters = filters.get_joined_filters(self._base_filters)
        count, lst = self.datamodel.query(joined_filters, order_column, order_direction, page=page, page_size=page_size)
        pks = self.datamodel.get_keys(lst)
        pks = [self._serialize_pk_if_composite(pk) for pk in pks]
        widgets['list'] = self.list_widget(label_columns=(self.label_columns), include_columns=(self.list_columns),
          value_columns=(self.datamodel.get_values(lst, self.list_columns)),
          order_columns=(self.order_columns),
          formatters_columns=(self.formatters_columns),
          page=page,
          page_size=page_size,
          count=count,
          pks=pks,
          actions=actions,
          filters=filters,
          modelview_name=(self.__class__.__name__))
        return widgets

    def _get_show_widget(self, pk, item, widgets=None, actions=None, show_fieldsets=None):
        widgets = widgets or {}
        actions = actions or self.actions
        show_fieldsets = show_fieldsets or self.show_fieldsets
        widgets['show'] = self.show_widget(pk=pk, label_columns=(self.label_columns),
          include_columns=(self.show_columns),
          value_columns=(self.datamodel.get_values_item(item, self.show_columns)),
          formatters_columns=(self.formatters_columns),
          actions=actions,
          fieldsets=show_fieldsets,
          modelview_name=(self.__class__.__name__))
        return widgets

    def _get_add_widget(self, form, exclude_cols=None, widgets=None):
        exclude_cols = exclude_cols or []
        widgets = widgets or {}
        widgets['add'] = self.add_widget(form=form, include_cols=(self.add_columns),
          exclude_cols=exclude_cols,
          fieldsets=(self.add_fieldsets))
        return widgets

    def _get_edit_widget(self, form, exclude_cols=None, widgets=None):
        exclude_cols = exclude_cols or []
        widgets = widgets or {}
        widgets['edit'] = self.edit_widget(form=form, include_cols=(self.edit_columns),
          exclude_cols=exclude_cols,
          fieldsets=(self.edit_fieldsets))
        return widgets

    def get_uninit_inner_views(self):
        """
            Will return a list with views that need to be initialized.
            Normally related_views from ModelView
        """
        return self.related_views

    def get_init_inner_views(self):
        """
            Get the list of related ModelViews after they have been initialized
        """
        return self._related_views

    def _list(self):
        """
            list function logic, override to implement different logic
            returns list and search widget
        """
        if get_order_args().get(self.__class__.__name__):
            order_column, order_direction = get_order_args().get(self.__class__.__name__)
        else:
            order_column, order_direction = ('', '')
        page = get_page_args().get(self.__class__.__name__)
        page_size = get_page_size_args().get(self.__class__.__name__)
        get_filter_args(self._filters)
        widgets = self._get_list_widget(filters=(self._filters), order_column=order_column,
          order_direction=order_direction,
          page=page,
          page_size=page_size)
        form = self.search_form.refresh()
        self.update_redirect()
        return self._get_search_widget(form=form, widgets=widgets)

    def _show(self, pk):
        """
            show function logic, override to implement different logic
            returns show and related list widget
        """
        pages = get_page_args()
        page_sizes = get_page_size_args()
        orders = get_order_args()
        item = self.datamodel.get(pk, self._base_filters)
        if not item:
            abort(404)
        widgets = self._get_show_widget(pk, item)
        self.update_redirect()
        return self._get_related_views_widgets(item, orders=orders, pages=pages,
          page_sizes=page_sizes,
          widgets=widgets)

    def _add(self):
        """
            Add function logic, override to implement different logic
            returns add widget or None
        """
        is_valid_form = True
        get_filter_args(self._filters)
        exclude_cols = self._filters.get_relation_cols()
        form = self.add_form.refresh()
        if request.method == 'POST':
            self._fill_form_exclude_cols(exclude_cols, form)
            if form.validate():
                self.process_form(form, True)
                item = self.datamodel.obj()
                form.populate_obj(item)
                try:
                    try:
                        self.pre_add(item)
                    except Exception as e:
                        flash(str(e), 'danger')
                    else:
                        if self.datamodel.add(item):
                            self.post_add(item)
                        flash(*self.datamodel.message)
                finally:
                    return

                return
            is_valid_form = False
        if is_valid_form:
            self.update_redirect()
        return self._get_add_widget(form=form, exclude_cols=exclude_cols)

    def _edit(self, pk):
        """
            Edit function logic, override to implement different logic
            returns Edit widget and related list or None
        """
        is_valid_form = True
        pages = get_page_args()
        page_sizes = get_page_size_args()
        orders = get_order_args()
        get_filter_args(self._filters)
        exclude_cols = self._filters.get_relation_cols()
        item = self.datamodel.get(pk, self._base_filters)
        if not item:
            abort(404)
        else:
            pk = self.datamodel.get_pk_value(item)
            if request.method == 'POST':
                form = self.edit_form.refresh(request.form)
                self._fill_form_exclude_cols(exclude_cols, form)
                form._id = pk
                if form.validate():
                    self.process_form(form, False)
                    form.populate_obj(item)
                    try:
                        try:
                            self.pre_update(item)
                        except Exception as e:
                            flash(str(e), 'danger')
                        else:
                            if self.datamodel.edit(item):
                                self.post_update(item)
                            flash(*self.datamodel.message)
                    finally:
                        return

                    return
                is_valid_form = False
            else:
                form = self.edit_form.refresh(obj=item)
                self.prefill_form(form, pk)
        widgets = self._get_edit_widget(form=form, exclude_cols=exclude_cols)
        widgets = self._get_related_views_widgets(item, filters={}, orders=orders,
          pages=pages,
          page_sizes=page_sizes,
          widgets=widgets)
        if is_valid_form:
            self.update_redirect()
        return widgets

    def _delete(self, pk):
        """
            Delete function logic, override to implement different logic
            deletes the record with primary_key = pk
            :param pk:
                record primary key to delete
        """
        item = self.datamodel.get(pk, self._base_filters)
        if not item:
            abort(404)
        try:
            self.pre_delete(item)
        except Exception as e:
            flash(str(e), 'danger')
        else:
            if self.datamodel.delete(item):
                self.post_delete(item)
            flash(*self.datamodel.message)
            self.update_redirect()

    def _serialize_pk_if_composite(self, pk):

        def date_serializer(obj):
            if isinstance(obj, datetime):
                return {'_type':'datetime',  'value':obj.isoformat()}
            if isinstance(obj, date):
                return {'_type':'date',  'value':obj.isoformat()}

        if self.datamodel.is_pk_composite():
            try:
                pk = json.dumps(pk, default=date_serializer)
            except:
                pass

        return pk

    def _deserialize_pk_if_composite(self, pk):

        def date_deserializer(obj):
            if '_type' not in obj:
                return obj
            else:
                from dateutil import parser
                if obj['_type'] == 'datetime':
                    return parser.parse(obj['value'])
                if obj['_type'] == 'date':
                    return parser.parse(obj['value']).date()
                return obj

        if self.datamodel.is_pk_composite():
            try:
                pk = json.loads(pk, object_hook=date_deserializer)
            except:
                pass

        return pk

    def _fill_form_exclude_cols(self, exclude_cols, form):
        """
            fill the form with the suppressed cols, generated from exclude_cols
        """
        for filter_key in exclude_cols:
            filter_value = self._filters.get_filter_value(filter_key)
            rel_obj = self.datamodel.get_related_obj(filter_key, filter_value)
            if hasattr(form, filter_key):
                field = getattr(form, filter_key)
                field.data = rel_obj

    def prefill_form(self, form, pk):
        """
            Override this, will be called only if the current action is rendering
            an edit form (a GET request), and is used to perform additional action to
            prefill the form.
            This is useful when you have added custom fields that depend on the
            database contents. Fields that were added by name of a normal column
            or relationship should work out of the box.
            example::
                def prefill_form(self, form, pk):
                    if form.email.data:
                        form.email_confirmation.data = form.email.data
        """
        pass

    def process_form(self, form, is_created):
        """
            Override this, will be called only if the current action is submitting
            a create/edit form (a POST request), and is used to perform additional
            action before the form is used to populate the item.
            By default does nothing.
            example::
                def process_form(self, form, is_created):
                    if not form.owner:
                        form.owner.data = 'n/a'
        """
        pass

    def pre_update(self, item):
        """
            Override this, this method is called before the update takes place.
            If an exception is raised by this method,
            the message is shown to the user and the update operation is
            aborted. Because of this behavior, it can be used as a way to
            implement more complex logic around updates. For instance
            allowing only the original creator of the object to update it.
        """
        pass

    def post_update(self, item):
        """
            Override this, will be called after update
        """
        pass

    def pre_add(self, item):
        """
            Override this, will be called before add.
            If an exception is raised by this method,
            the message is shown to the user and the add operation is aborted.
        """
        pass

    def post_add(self, item):
        """
            Override this, will be called after update
        """
        pass

    def pre_delete(self, item):
        """
            Override this, will be called before delete
            If an exception is raised by this method,
            the message is shown to the user and the delete operation is
            aborted. Because of this behavior, it can be used as a way to
            implement more complex logic around deletes. For instance
            allowing only the original creator of the object to delete it.
        """
        pass

    def post_delete(self, item):
        """
            Override this, will be called after delete
        """
        pass