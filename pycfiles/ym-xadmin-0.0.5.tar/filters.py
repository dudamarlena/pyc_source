# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: G:\python\hhwork\extra_apps\xadmin\plugins\filters.py
# Compiled at: 2019-01-06 19:47:42
import operator
from functools import reduce
from django.contrib.admin.utils import get_fields_from_path, lookup_needs_distinct
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured, ValidationError
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db.models.sql.query import LOOKUP_SEP, QUERY_TERMS
from django.template import loader
from django.utils import six
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from future.utils import iteritems
from xadmin import widgets
from xadmin.filters import manager as filter_manager, FILTER_PREFIX, SEARCH_VAR, DateFieldListFilter, RelatedFieldSearchFilter
from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.util import is_related_field
from xadmin.views import BaseAdminPlugin, ListAdminView

class IncorrectLookupParameters(Exception):
    pass


class FilterPlugin(BaseAdminPlugin):
    list_filter = ()
    search_fields = ()
    free_query_filter = True

    def lookup_allowed(self, lookup, value):
        model = self.model
        for l in model._meta.related_fkey_lookups:
            for k, v in widgets.url_params_from_lookup_dict(l).items():
                if k == lookup and v == value:
                    return True

        parts = lookup.split(LOOKUP_SEP)
        if len(parts) > 1 and parts[(-1)] in QUERY_TERMS:
            parts.pop()
        rel_name = None
        for part in parts[:-1]:
            try:
                field = model._meta.get_field(part)
            except FieldDoesNotExist:
                return True

            if hasattr(field, 'rel'):
                model = field.rel.to
                rel_name = field.rel.get_related_field().name
            elif is_related_field(field):
                model = field.model
                rel_name = model._meta.pk.name
            else:
                rel_name = None

        if rel_name and len(parts) > 1 and parts[(-1)] == rel_name:
            parts.pop()
        if len(parts) == 1:
            return True
        else:
            clean_lookup = LOOKUP_SEP.join(parts)
            return clean_lookup in self.list_filter

    def get_list_queryset(self, queryset):
        lookup_params = dict([ (smart_str(k)[len(FILTER_PREFIX):], v) for k, v in self.admin_view.params.items() if smart_str(k).startswith(FILTER_PREFIX) and v != ''
                             ])
        for p_key, p_val in iteritems(lookup_params):
            if p_val == 'False':
                lookup_params[p_key] = False

        use_distinct = False
        self.admin_view.has_query_param = bool(lookup_params)
        self.admin_view.clean_query_url = self.admin_view.get_query_string(remove=[ k for k in self.request.GET.keys() if k.startswith(FILTER_PREFIX)
                                                                                  ])
        if not self.free_query_filter:
            for key, value in lookup_params.items():
                if not self.lookup_allowed(key, value):
                    raise SuspiciousOperation('Filtering by %s not allowed' % key)

        self.filter_specs = []
        if self.list_filter:
            for list_filter in self.list_filter:
                if callable(list_filter):
                    spec = list_filter(self.request, lookup_params, self.model, self)
                else:
                    field_path = None
                    field_parts = []
                    if isinstance(list_filter, (tuple, list)):
                        field, field_list_filter_class = list_filter
                    else:
                        field, field_list_filter_class = list_filter, filter_manager.create
                    if not isinstance(field, models.Field):
                        field_path = field
                        field_parts = get_fields_from_path(self.model, field_path)
                        field = field_parts[(-1)]
                    spec = field_list_filter_class(field, self.request, lookup_params, self.model, self.admin_view, field_path=field_path)
                    if len(field_parts) > 1:
                        spec.title = '%s %s' % (field_parts[(-2)].name, spec.title)
                    use_distinct = use_distinct or lookup_needs_distinct(self.opts, field_path)
                if spec and spec.has_output():
                    try:
                        new_qs = spec.do_filte(queryset)
                    except ValidationError as e:
                        new_qs = None
                        self.admin_view.message_user(_('<b>Filtering error:</b> %s') % e.messages[0], 'error')

                    if new_qs is not None:
                        queryset = new_qs
                    self.filter_specs.append(spec)

        self.has_filters = bool(self.filter_specs)
        self.admin_view.filter_specs = self.filter_specs
        obj = filter(lambda f: f.is_used, self.filter_specs)
        if six.PY3:
            obj = list(obj)
        self.admin_view.used_filter_num = len(obj)
        try:
            for key, value in lookup_params.items():
                use_distinct = use_distinct or lookup_needs_distinct(self.opts, key)

        except FieldDoesNotExist as e:
            raise IncorrectLookupParameters(e)

        try:
            if isinstance(queryset, models.query.QuerySet) and lookup_params:
                new_lookup_parames = dict()
                try:
                    loop = lookup_params.iteritems()
                except Exception as e:
                    loop = lookup_params.items()

                for k, v in loop:
                    list_v = v.split(',')
                    if len(list_v) > 0:
                        new_lookup_parames.update({k: list_v})
                    else:
                        new_lookup_parames.update({k: v})

                queryset = queryset.filter(**new_lookup_parames)
        except (SuspiciousOperation, ImproperlyConfigured):
            raise
        except Exception as e:
            raise IncorrectLookupParameters(e)

        if not isinstance(queryset, models.query.QuerySet):
            pass
        query = self.request.GET.get(SEARCH_VAR, '')

        def construct_search(field_name):
            if field_name.startswith('^'):
                return '%s__istartswith' % field_name[1:]
            else:
                if field_name.startswith('='):
                    return '%s__iexact' % field_name[1:]
                if field_name.startswith('@'):
                    return '%s__search' % field_name[1:]
                return '%s__icontains' % field_name

        if self.search_fields and query:
            orm_lookups = [ construct_search(str(search_field)) for search_field in self.search_fields ]
            for bit in query.split():
                or_queries = [ models.Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups ]
                queryset = queryset.filter(reduce(operator.or_, or_queries))

            if not use_distinct:
                for search_spec in orm_lookups:
                    if lookup_needs_distinct(self.opts, search_spec):
                        use_distinct = True
                        break

            self.admin_view.search_query = query
        if use_distinct:
            return queryset.distinct()
        else:
            return queryset
            return

    def get_media(self, media):
        arr = filter(lambda s: isinstance(s, DateFieldListFilter), self.filter_specs)
        if six.PY3:
            arr = list(arr)
        if bool(arr):
            media = media + self.vendor('datepicker.css', 'datepicker.js', 'xadmin.widget.datetime.js')
        arr = filter(lambda s: isinstance(s, RelatedFieldSearchFilter), self.filter_specs)
        if six.PY3:
            arr = list(arr)
        if bool(arr):
            media = media + self.vendor('select.js', 'select.css', 'xadmin.widget.select.js')
        return media + self.vendor('xadmin.plugin.filters.js')

    def block_nav_menu(self, context, nodes):
        if self.has_filters:
            nodes.append(loader.render_to_string('xadmin/blocks/model_list.nav_menu.filters.html', context=get_context_dict(context)))

    def block_nav_form(self, context, nodes):
        if self.search_fields:
            context = get_context_dict(context or {})
            context.update({'search_var': SEARCH_VAR, 
               'remove_search_url': self.admin_view.get_query_string(remove=[SEARCH_VAR]), 
               'search_form_params': self.admin_view.get_form_params(remove=[SEARCH_VAR])})
            nodes.append(loader.render_to_string('xadmin/blocks/model_list.nav_form.search_form.html', context=context))


site.register_plugin(FilterPlugin, ListAdminView)