# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\hhwork\extra_apps\xadmin\plugins\quickfilter.py
# Compiled at: 2019-04-17 23:57:58
# Size of source mod 2**32: 7424 bytes
"""
Created on Mar 26, 2014

@author: LAB_ADM
"""
from future.utils import iteritems
from django.utils import six
import django.utils.translation as _
from xadmin.filters import manager, MultiSelectFieldListFilter
from xadmin.plugins.filters import *
from xadmin.util import is_related_field

@manager.register
class QuickFilterMultiSelectFieldListFilter(MultiSelectFieldListFilter):
    __doc__ = ' Delegates the filter to the default filter and ors the results of each\n     \n    Lists the distinct values of each field as a checkbox\n    Uses the default spec for each \n     \n    '
    template = 'xadmin/filters/quickfilter.html'


class QuickFilterPlugin(BaseAdminPlugin):
    __doc__ = ' Add a filter menu to the left column of the page '
    list_quick_filter = ()
    quickfilter = {}
    search_fields = ()
    free_query_filter = True

    def init_request(self, *args, **kwargs):
        menu_style_accordian = hasattr(self.admin_view, 'menu_style') and self.admin_view.menu_style == 'accordion'
        return bool(self.list_quick_filter) and not menu_style_accordian

    def get_media(self, media):
        return media + self.vendor('xadmin.plugin.quickfilter.js', 'xadmin.plugin.quickfilter.css')

    def lookup_allowed(self, lookup, value):
        model = self.model
        for l in model._meta.related_fkey_lookups:
            for k, v in widgets.url_params_from_lookup_dict(l).items():
                if k == lookup and v == value:
                    return True

        parts = lookup.split(LOOKUP_SEP)
        if len(parts) > 1:
            if parts[(-1)] in QUERY_TERMS:
                parts.pop()
        rel_name = None
        for part in parts[:-1]:
            try:
                field = model._meta.get_field(part)
            except FieldDoesNotExist:
                return True
            else:
                if hasattr(field, 'rel'):
                    model = field.rel.to
                    rel_name = field.rel.get_related_field().name
                elif is_related_field(field):
                    model = field.model
                    rel_name = model._meta.pk.name
                else:
                    rel_name = None

        if rel_name:
            if len(parts) > 1:
                if parts[(-1)] == rel_name:
                    parts.pop()
        if len(parts) == 1:
            return True
        clean_lookup = LOOKUP_SEP.join(parts)
        return clean_lookup in self.list_quick_filter

    def get_list_queryset(self, queryset):
        lookup_params = dict([(smart_str(k)[len(FILTER_PREFIX):], v) for k, v in self.admin_view.params.items() if smart_str(k).startswith(FILTER_PREFIX) if v != ''])
        for p_key, p_val in iteritems(lookup_params):
            if p_val == 'False':
                lookup_params[p_key] = False

        use_distinct = False
        if not hasattr(self.admin_view, 'quickfilter'):
            self.admin_view.quickfilter = {}
        self.admin_view.quickfilter['has_query_param'] = bool(lookup_params)
        self.admin_view.quickfilter['clean_query_url'] = self.admin_view.get_query_string(remove=[k for k in self.request.GET.keys() if k.startswith(FILTER_PREFIX)])
        if not self.free_query_filter:
            for key, value in lookup_params.items():
                if not self.lookup_allowed(key, value):
                    raise SuspiciousOperation('Filtering by %s not allowed' % key)

        self.filter_specs = []
        if self.list_quick_filter:
            for list_quick_filter in self.list_quick_filter:
                field_path = None
                field_order_by = None
                field_limit = None
                field_parts = []
                sort_key = None
                cache_config = None
                if type(list_quick_filter) == dict and 'field' in list_quick_filter:
                    field = list_quick_filter['field']
                    if 'order_by' in list_quick_filter:
                        field_order_by = list_quick_filter['order_by']
                    if 'limit' in list_quick_filter:
                        field_limit = list_quick_filter['limit']
                    if 'sort' in list_quick_filter:
                        if callable(list_quick_filter['sort']):
                            sort_key = list_quick_filter['sort']
                    if 'cache' in list_quick_filter and type(list_quick_filter) == dict:
                        cache_config = list_quick_filter['cache']
                else:
                    field = list_quick_filter
                if not isinstance(field, models.Field):
                    field_path = field
                    field_parts = get_fields_from_path(self.model, field_path)
                    field = field_parts[(-1)]
                spec = QuickFilterMultiSelectFieldListFilter(field, (self.request), lookup_params, (self.model), (self.admin_view), field_path=field_path, field_order_by=field_order_by, field_limit=field_limit, sort_key=sort_key, cache_config=cache_config)
                if len(field_parts) > 1:
                    spec.title = '%s %s' % (field_parts[(-2)].name, spec.title)
                use_distinct = True
                if spec and spec.has_output():
                    try:
                        new_qs = spec.do_filte(queryset)
                    except ValidationError as e:
                        try:
                            new_qs = None
                            self.admin_view.message_user(_('<b>Filtering error:</b> %s') % e.messages[0], 'error')
                        finally:
                            e = None
                            del e

                    if new_qs is not None:
                        queryset = new_qs
                    self.filter_specs.append(spec)

        self.has_filters = bool(self.filter_specs)
        self.admin_view.quickfilter['filter_specs'] = self.filter_specs
        obj = filter(lambda f: f.is_used, self.filter_specs)
        if six.PY3:
            obj = list(obj)
        self.admin_view.quickfilter['used_filter_num'] = len(obj)
        if use_distinct:
            return queryset.distinct()
        return queryset

    def block_left_navbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/blocks/modal_list.left_navbar.quickfilter.html', get_context_dict(context)))


site.register_plugin(QuickFilterPlugin, ListAdminView)