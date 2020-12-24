# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\hhwork\extra_apps\xadmin\views\list.py
# Compiled at: 2019-04-17 23:57:58
# Size of source mod 2**32: 26203 bytes
from __future__ import absolute_import
from collections import OrderedDict
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import InvalidPage, Paginator
from django.core.urlresolvers import NoReverseMatch
from django.db import models
from django.http import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.utils import six
from django.utils.encoding import force_text, smart_text
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
import django.utils.translation as _
from xadmin.util import lookup_field, display_for_field, label_for_field, boolean_icon
from .base import ModelAdminView, filter_hook, inclusion_tag, csrf_protect_m
ALL_VAR = 'all'
ORDER_VAR = 'o'
PAGE_VAR = 'p'
TO_FIELD_VAR = 't'
COL_LIST_VAR = '_cols'
ERROR_FLAG = 'e'
DOT = '.'
EMPTY_CHANGELIST_VALUE = _('Null')

class FakeMethodField(object):
    __doc__ = '\n    This class used when a column is an model function, wrap function as a fake field to display in select columns.\n    '

    def __init__(self, name, verbose_name):
        self.name = name
        self.verbose_name = verbose_name
        self.primary_key = False


class ResultRow(dict):
    pass


class ResultItem(object):

    def __init__(self, field_name, row):
        self.classes = []
        self.text = '&nbsp;'
        self.wraps = []
        self.tag = 'td'
        self.tag_attrs = []
        self.allow_tags = False
        self.btns = []
        self.menus = []
        self.is_display_link = False
        self.row = row
        self.field_name = field_name
        self.field = None
        self.attr = None
        self.value = None

    @property
    def label(self):
        text = mark_safe(self.text) if self.allow_tags else conditional_escape(self.text)
        if force_text(text) == '':
            text = mark_safe('&nbsp;')
        for wrap in self.wraps:
            text = mark_safe(wrap % text)

        return text

    @property
    def tagattrs(self):
        return mark_safe('%s%s' % (self.tag_attrs and ' '.join(self.tag_attrs) or '',
         self.classes and ' class="%s"' % ' '.join(self.classes) or ''))


class ResultHeader(ResultItem):

    def __init__(self, field_name, row):
        super(ResultHeader, self).__init__(field_name, row)
        self.tag = 'th'
        self.tag_attrs = ['scope="col"']
        self.sortable = False
        self.allow_tags = True
        self.sorted = False
        self.ascending = None
        self.sort_priority = None
        self.url_primary = None
        self.url_remove = None
        self.url_toggle = None


class ListAdminView(ModelAdminView):
    __doc__ = '\n    Display models objects view. this class has ordering and simple filter features.\n    '
    list_display = ('__str__', )
    list_display_links = ()
    list_display_links_details = False
    list_select_related = None
    list_per_page = 50
    list_max_show_all = 200
    list_exclude = ()
    search_fields = ()
    paginator_class = Paginator
    ordering = None
    object_list_template = None

    def init_request(self, *args, **kwargs):
        if not self.has_view_permission():
            raise PermissionDenied
        request = self.request
        request.session['LIST_QUERY'] = (self.model_info, self.request.META['QUERY_STRING'])
        self.pk_attname = self.opts.pk.attname
        self.lookup_opts = self.opts
        self.list_display = self.get_list_display()
        self.list_display_links = self.get_list_display_links()
        try:
            self.page_num = int(request.GET.get(PAGE_VAR, 0))
        except ValueError:
            self.page_num = 0

        self.show_all = ALL_VAR in request.GET
        self.to_field = request.GET.get(TO_FIELD_VAR)
        self.params = dict(request.GET.items())
        if PAGE_VAR in self.params:
            del self.params[PAGE_VAR]
        if ERROR_FLAG in self.params:
            del self.params[ERROR_FLAG]

    @filter_hook
    def get_list_display(self):
        """
        Return a sequence containing the fields to be displayed on the list.
        """
        self.base_list_display = COL_LIST_VAR in self.request.GET and self.request.GET[COL_LIST_VAR] != '' and self.request.GET[COL_LIST_VAR].split('.') or self.list_display
        return list(self.base_list_display)

    @filter_hook
    def get_list_display_links(self):
        """
        Return a sequence containing the fields to be displayed as links
        on the changelist. The list_display parameter is the list of fields
        returned by get_list_display().
        """
        return self.list_display_links or self.list_display or self.list_display_links
        return list(self.list_display)[:1]

    def make_result_list(self):
        self.base_queryset = self.queryset()
        self.list_queryset = self.get_list_queryset()
        self.ordering_field_columns = self.get_ordering_field_columns()
        self.paginator = self.get_paginator()
        self.result_count = self.paginator.count
        self.can_show_all = self.result_count <= self.list_max_show_all
        self.multi_page = self.result_count > self.list_per_page
        if self.show_all:
            self.result_list = self.can_show_all or self.multi_page or self.list_queryset._clone()
        else:
            try:
                self.result_list = self.paginator.page(self.page_num + 1).object_list
            except InvalidPage:
                if ERROR_FLAG in self.request.GET.keys():
                    return SimpleTemplateResponse('xadmin/views/invalid_setup.html', {'title': _('Database error')})
                return HttpResponseRedirect(self.request.path + '?' + ERROR_FLAG + '=1')

            self.has_more = self.result_count > self.list_per_page * self.page_num + len(self.result_list)

    @filter_hook
    def get_result_list(self):
        return self.make_result_list()

    @filter_hook
    def post_result_list(self):
        return self.make_result_list()

    @filter_hook
    def get_list_queryset(self):
        """
        Get model queryset. The query has been filted and ordered.
        """
        queryset = self.queryset()
        if not queryset.query.select_related:
            if self.list_select_related:
                queryset = queryset.select_related()
            else:
                if self.list_select_related is None:
                    related_fields = []
                    for field_name in self.list_display:
                        try:
                            field = self.opts.get_field(field_name)
                        except models.FieldDoesNotExist:
                            pass
                        else:
                            if isinstance(field.rel, models.ManyToOneRel):
                                related_fields.append(field_name)

                    if related_fields:
                        queryset = (queryset.select_related)(*related_fields)
        queryset = (queryset.order_by)(*self.get_ordering())
        return queryset

    def _get_default_ordering(self):
        ordering = []
        if self.ordering:
            ordering = self.ordering
        else:
            if self.opts.ordering:
                ordering = self.opts.ordering
        return ordering

    @filter_hook
    def get_ordering_field(self, field_name):
        """
        Returns the proper model field name corresponding to the given
        field_name to use for ordering. field_name may either be the name of a
        proper model field or the name of a method (on the admin or model) or a
        callable with the 'admin_order_field' attribute. Returns None if no
        proper model field name can be matched.
        """
        try:
            field = self.opts.get_field(field_name)
            return field.name
        except models.FieldDoesNotExist:
            if callable(field_name):
                attr = field_name
            else:
                if hasattr(self, field_name):
                    attr = getattr(self, field_name)
                else:
                    attr = getattr(self.model, field_name)
            return getattr(attr, 'admin_order_field', None)

    @filter_hook
    def get_ordering(self):
        ordering = list(super(ListAdminView, self).get_ordering() or self._get_default_ordering())
        if ORDER_VAR in self.params:
            if self.params[ORDER_VAR]:
                ordering = [pfx + self.get_ordering_field(field_name) for n, pfx, field_name in map(lambda p: p.rpartition('-'), self.params[ORDER_VAR].split('.')) if self.get_ordering_field(field_name)]
        pk_name = self.opts.pk.name
        if not set(ordering) & set(['pk', '-pk', pk_name, '-' + pk_name]):
            ordering.append('-pk')
        return ordering

    @filter_hook
    def get_ordering_field_columns--- This code section failed: ---

 L. 315         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_default_ordering
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  STORE_FAST               'ordering'

 L. 316         8  LOAD_GLOBAL              OrderedDict
               10  CALL_FUNCTION_0       0  '0 positional arguments'
               12  STORE_FAST               'ordering_fields'

 L. 317        14  LOAD_GLOBAL              ORDER_VAR
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                params
               20  COMPARE_OP               not-in
               22  POP_JUMP_IF_TRUE     34  'to 34'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                params
               28  LOAD_GLOBAL              ORDER_VAR
               30  BINARY_SUBSCR    
               32  POP_JUMP_IF_TRUE    122  'to 122'
             34_0  COME_FROM            22  '22'

 L. 321        34  SETUP_LOOP          184  'to 184'
               36  LOAD_FAST                'ordering'
               38  GET_ITER         
               40  FOR_ITER            118  'to 118'
               42  STORE_FAST               'field'

 L. 322        44  LOAD_FAST                'field'
               46  LOAD_METHOD              startswith
               48  LOAD_STR                 '-'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  POP_JUMP_IF_FALSE    72  'to 72'

 L. 323        54  LOAD_FAST                'field'
               56  LOAD_CONST               1
               58  LOAD_CONST               None
               60  BUILD_SLICE_2         2 
               62  BINARY_SUBSCR    
               64  STORE_FAST               'field'

 L. 324        66  LOAD_STR                 'desc'
               68  STORE_FAST               'order_type'
               70  JUMP_FORWARD         76  'to 76'
             72_0  COME_FROM            52  '52'

 L. 326        72  LOAD_STR                 'asc'
               74  STORE_FAST               'order_type'
             76_0  COME_FROM            70  '70'

 L. 327        76  SETUP_LOOP          116  'to 116'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                list_display
               82  GET_ITER         
             84_0  COME_FROM           100  '100'
               84  FOR_ITER            114  'to 114'
               86  STORE_FAST               'attr'

 L. 328        88  LOAD_FAST                'self'
               90  LOAD_METHOD              get_ordering_field
               92  LOAD_FAST                'attr'
               94  CALL_METHOD_1         1  '1 positional argument'
               96  LOAD_FAST                'field'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE    84  'to 84'

 L. 329       102  LOAD_FAST                'order_type'
              104  LOAD_FAST                'ordering_fields'
              106  LOAD_FAST                'field'
              108  STORE_SUBSCR     

 L. 330       110  BREAK_LOOP       
              112  JUMP_BACK            84  'to 84'
              114  POP_BLOCK        
            116_0  COME_FROM_LOOP       76  '76'
              116  JUMP_BACK            40  'to 40'
              118  POP_BLOCK        
              120  JUMP_FORWARD        184  'to 184'
            122_0  COME_FROM            32  '32'

 L. 332       122  SETUP_LOOP          184  'to 184'
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                params
              128  LOAD_GLOBAL              ORDER_VAR
              130  BINARY_SUBSCR    
              132  LOAD_METHOD              split
              134  LOAD_STR                 '.'
              136  CALL_METHOD_1         1  '1 positional argument'
              138  GET_ITER         
              140  FOR_ITER            182  'to 182'
              142  STORE_FAST               'p'

 L. 333       144  LOAD_FAST                'p'
              146  LOAD_METHOD              rpartition
              148  LOAD_STR                 '-'
              150  CALL_METHOD_1         1  '1 positional argument'
              152  UNPACK_SEQUENCE_3     3 
              154  STORE_FAST               'none'
              156  STORE_FAST               'pfx'
              158  STORE_FAST               'field_name'

 L. 334       160  LOAD_FAST                'pfx'
              162  LOAD_STR                 '-'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   172  'to 172'
              168  LOAD_STR                 'desc'
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           166  '166'
              172  LOAD_STR                 'asc'
            174_0  COME_FROM           170  '170'
              174  LOAD_FAST                'ordering_fields'
              176  LOAD_FAST                'field_name'
              178  STORE_SUBSCR     
              180  JUMP_BACK           140  'to 140'
              182  POP_BLOCK        
            184_0  COME_FROM_LOOP      122  '122'
            184_1  COME_FROM           120  '120'
            184_2  COME_FROM_LOOP       34  '34'

 L. 335       184  LOAD_FAST                'ordering_fields'
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 184_2

    def get_check_field_url(self, f):
        """
        Return the select column menu items link.
        We must use base_list_display, because list_display maybe changed by plugins.
        """
        fields = [fd for fd in self.base_list_display if fd != f.name]
        if len(self.base_list_display) == len(fields):
            if f.primary_key:
                fields.insert(0, f.name)
            else:
                fields.append(f.name)
        return self.get_query_string({COL_LIST_VAR: '.'.join(fields)})

    def get_model_method_fields(self):
        """
        Return the fields info defined in model. use FakeMethodField class wrap method as a db field.
        """
        methods = []
        for name in dir(self):
            try:
                if getattr(getattr(self, name), 'is_column', False):
                    methods.append((name, getattr(self, name)))
            except:
                pass

        return [FakeMethodField(name, getattr(method, 'short_description', capfirst(name.replace('_', ' ')))) for name, method in methods]

    @filter_hook
    def get_context(self):
        self.title = _('%s List') % force_text(self.opts.verbose_name)
        model_fields = [(f, f.name in self.list_display, self.get_check_field_url(f)) for f in list(self.opts.fields) + self.get_model_method_fields() if f.name not in self.list_exclude]
        new_context = {'model_name':force_text(self.opts.verbose_name_plural), 
         'title':self.title, 
         'cl':self, 
         'model_fields':model_fields, 
         'clean_select_field_url':self.get_query_string(remove=[COL_LIST_VAR]), 
         'has_add_permission':self.has_add_permission(), 
         'app_label':self.app_label, 
         'brand_name':self.opts.verbose_name_plural, 
         'brand_icon':self.get_model_icon(self.model), 
         'add_url':self.model_admin_url('add'), 
         'result_headers':self.result_headers(), 
         'results':self.results()}
        context = super(ListAdminView, self).get_context()
        context.update(new_context)
        return context

    @filter_hook
    def get_response(self, context, *args, **kwargs):
        pass

    @csrf_protect_m
    @filter_hook
    def get(self, request, *args, **kwargs):
        """
        The 'change list' admin view for this model.
        """
        response = self.get_result_list()
        if response:
            return response
        context = self.get_context()
        context.update(kwargs or {})
        response = (self.get_response)(context, *args, **kwargs)
        return response or TemplateResponse(request, self.object_list_template or self.get_template_list('views/model_list.html'), context)

    @filter_hook
    def post_response(self, *args, **kwargs):
        pass

    @csrf_protect_m
    @filter_hook
    def post(self, request, *args, **kwargs):
        return self.post_result_list() or (self.post_response)(*args, **kwargs) or (self.get)(request, *args, **kwargs)

    @filter_hook
    def get_paginator(self):
        return self.paginator_class(self.list_queryset, self.list_per_page, 0, True)

    @filter_hook
    def get_page_number(self, i):
        if i == DOT:
            return mark_safe('<span class="dot-page">...</span> ')
        if i == self.page_num:
            return mark_safe('<span class="this-page">%d</span> ' % (i + 1))
        return mark_safe('<a href="%s"%s>%d</a> ' % (escape(self.get_query_string({PAGE_VAR: i})), i == self.paginator.num_pages - 1 and ' class="end"' or '', i + 1))

    @filter_hook
    def result_header(self, field_name, row):
        ordering_field_columns = self.ordering_field_columns
        item = ResultHeader(field_name, row)
        text, attr = label_for_field(field_name, (self.model), model_admin=self,
          return_attr=True)
        item.text = text
        item.attr = attr
        if attr:
            if not getattr(attr, 'admin_order_field', None):
                return item
        th_classes = ['sortable']
        order_type = ''
        new_order_type = 'desc'
        sort_priority = 0
        sorted = False
        if field_name in ordering_field_columns:
            sorted = True
            order_type = ordering_field_columns.get(field_name).lower()
            arr = ordering_field_columns.keys()
            if six.PY3:
                arr = list(arr)
            sort_priority = arr.index(field_name) + 1
            th_classes.append('sorted %sending' % order_type)
            new_order_type = {'asc':'desc',  'desc':'asc'}[order_type]
        o_list_asc = []
        o_list_desc = []
        o_list_remove = []
        o_list_toggle = []
        make_qs_param = lambda t, n: ('-' if t == 'desc' else '') + str(n)
        for j, ot in ordering_field_columns.items():
            if j == field_name:
                param = make_qs_param(new_order_type, j)
                o_list_asc.insert(0, j)
                o_list_desc.insert(0, '-' + j)
                o_list_toggle.append(param)
            else:
                param = make_qs_param(ot, j)
                o_list_asc.append(param)
                o_list_desc.append(param)
                o_list_toggle.append(param)
                o_list_remove.append(param)

        if field_name not in ordering_field_columns:
            o_list_asc.insert(0, field_name)
            o_list_desc.insert(0, '-' + field_name)
        item.sorted = sorted
        item.sortable = True
        item.ascending = order_type == 'asc'
        item.sort_priority = sort_priority
        menus = [
         (
          'asc', o_list_asc, 'caret-up', _('Sort ASC')),
         (
          'desc', o_list_desc, 'caret-down', _('Sort DESC'))]
        if sorted:
            row['num_sorted_fields'] = row['num_sorted_fields'] + 1
            menus.append((None, o_list_remove, 'times', _('Cancel Sort')))
            item.btns.append('<a class="toggle" href="%s"><i class="fa fa-%s"></i></a>' % (
             self.get_query_string({ORDER_VAR: '.'.join(o_list_toggle)}), 'sort-up' if order_type == 'asc' else 'sort-down'))
        item.menus.extend(['<li%s><a href="%s" class="active"><i class="fa fa-%s"></i> %s</a></li>' % (' class="active"' if (sorted and order_type == i[0]) else '', self.get_query_string({ORDER_VAR: '.'.join(i[1])}), i[2], i[3]) for i in menus])
        item.classes.extend(th_classes)
        return item

    @filter_hook
    def result_headers(self):
        """
        Generates the list column headers.
        """
        row = ResultRow
        row['num_sorted_fields'] = 0
        row.cells = [self.result_header(field_name, row) for field_name in self.list_display]
        return row

    @filter_hook
    def result_item(self, obj, field_name, row):
        """
        Generates the actual list of data.
        """
        item = ResultItem(field_name, row)
        try:
            f, attr, value = lookup_field(field_name, obj, self)
        except (AttributeError, ObjectDoesNotExist, NoReverseMatch):
            item.text = mark_safe("<span class='text-muted'>%s</span>" % EMPTY_CHANGELIST_VALUE)

        if f is None:
            item.allow_tags = getattr(attr, 'allow_tags', False)
            boolean = getattr(attr, 'boolean', False)
            if boolean:
                item.allow_tags = True
                item.text = boolean_icon(value)
            else:
                item.text = smart_text(value)
        else:
            if isinstance(f.rel, models.ManyToOneRel):
                field_val = getattr(obj, f.name)
                if field_val is None:
                    item.text = mark_safe("<span class='text-muted'>%s</span>" % EMPTY_CHANGELIST_VALUE)
                else:
                    item.text = field_val
            else:
                item.text = display_for_field(value, f)
            if not isinstance(f, models.DateField):
                if isinstance(f, models.TimeField) or isinstance(f, models.ForeignKey):
                    item.classes.append('nowrap')
                item.field = f
                item.attr = attr
                item.value = value
            elif not item.row['is_display_first'] or self.list_display_links:
                if field_name in self.list_display_links:
                    item.row['is_display_first'] = False
                    item.is_display_link = True
                    if self.list_display_links_details:
                        item_res_uri = self.model_admin_url('detail', getattr(obj, self.pk_attname))
                        if item_res_uri:
                            if self.has_change_permission(obj):
                                edit_url = self.model_admin_url('change', getattr(obj, self.pk_attname))
                            else:
                                edit_url = ''
                            item.wraps.append('<a data-res-uri="%s" data-edit-uri="%s" class="details-handler" rel="tooltip" title="%s">%%s</a>' % (
                             item_res_uri, edit_url, _('Details of %s') % str(obj)))
                    else:
                        url = self.url_for_result(obj)
                        item.wraps.append('<a href="%s">%%s</a>' % url)
            return item

    @filter_hook
    def result_row(self, obj):
        row = ResultRow
        row['is_display_first'] = True
        row['object'] = obj
        row.cells = [self.result_item(obj, field_name, row) for field_name in self.list_display]
        return row

    @filter_hook
    def results(self):
        results = []
        for obj in self.result_list:
            results.append(self.result_row(obj))

        return results

    @filter_hook
    def url_for_result(self, result):
        return self.get_object_url(result)

    @filter_hook
    def get_media(self):
        media = super(ListAdminView, self).get_media() + self.vendor('xadmin.page.list.js', 'xadmin.page.form.js')
        if self.list_display_links_details:
            media += self.vendor('xadmin.plugin.details.js', 'xadmin.form.css')
        return media

    @inclusion_tag('xadmin/includes/pagination.html')
    def block_pagination--- This code section failed: ---

 L. 618         0  LOAD_FAST                'self'
                2  LOAD_ATTR                paginator
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                page_num
                8  ROT_TWO          
               10  STORE_FAST               'paginator'
               12  STORE_FAST               'page_num'

 L. 621        14  LOAD_FAST                'self'
               16  LOAD_ATTR                show_all
               18  UNARY_NOT        
               20  POP_JUMP_IF_TRUE     30  'to 30'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                can_show_all
               26  UNARY_NOT        
               28  JUMP_IF_FALSE_OR_POP    34  'to 34'
             30_0  COME_FROM            20  '20'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                multi_page
             34_0  COME_FROM            28  '28'
               34  STORE_FAST               'pagination_required'

 L. 622        36  LOAD_FAST                'pagination_required'
               38  POP_JUMP_IF_TRUE     46  'to 46'

 L. 623        40  BUILD_LIST_0          0 
               42  STORE_FAST               'page_range'
               44  JUMP_FORWARD        292  'to 292'
             46_0  COME_FROM            38  '38'

 L. 625        46  LOAD_CONST               5
               48  LOAD_CONST               3
               50  LOAD_CONST               ('normal', 'small')
               52  BUILD_CONST_KEY_MAP_2     2 
               54  LOAD_METHOD              get
               56  LOAD_FAST                'page_type'
               58  LOAD_CONST               3
               60  CALL_METHOD_2         2  '2 positional arguments'
               62  STORE_FAST               'ON_EACH_SIDE'

 L. 626        64  LOAD_CONST               2
               66  STORE_FAST               'ON_ENDS'

 L. 630        68  LOAD_FAST                'paginator'
               70  LOAD_ATTR                num_pages
               72  LOAD_CONST               10
               74  COMPARE_OP               <=
               76  POP_JUMP_IF_FALSE    90  'to 90'

 L. 631        78  LOAD_GLOBAL              range
               80  LOAD_FAST                'paginator'
               82  LOAD_ATTR                num_pages
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  STORE_FAST               'page_range'
               88  JUMP_FORWARD        292  'to 292'
             90_0  COME_FROM            76  '76'

 L. 636        90  BUILD_LIST_0          0 
               92  STORE_FAST               'page_range'

 L. 637        94  LOAD_FAST                'page_num'
               96  LOAD_FAST                'ON_EACH_SIDE'
               98  LOAD_FAST                'ON_ENDS'
              100  BINARY_ADD       
              102  COMPARE_OP               >
              104  POP_JUMP_IF_FALSE   162  'to 162'

 L. 638       106  LOAD_FAST                'page_range'
              108  LOAD_METHOD              extend
              110  LOAD_GLOBAL              range
              112  LOAD_CONST               0
              114  LOAD_FAST                'ON_EACH_SIDE'
              116  LOAD_CONST               1
              118  BINARY_SUBTRACT  
              120  CALL_FUNCTION_2       2  '2 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  POP_TOP          

 L. 639       126  LOAD_FAST                'page_range'
              128  LOAD_METHOD              append
              130  LOAD_GLOBAL              DOT
              132  CALL_METHOD_1         1  '1 positional argument'
              134  POP_TOP          

 L. 640       136  LOAD_FAST                'page_range'
              138  LOAD_METHOD              extend

 L. 641       140  LOAD_GLOBAL              range
              142  LOAD_FAST                'page_num'
              144  LOAD_FAST                'ON_EACH_SIDE'
              146  BINARY_SUBTRACT  
              148  LOAD_FAST                'page_num'
              150  LOAD_CONST               1
              152  BINARY_ADD       
              154  CALL_FUNCTION_2       2  '2 positional arguments'
              156  CALL_METHOD_1         1  '1 positional argument'
              158  POP_TOP          
              160  JUMP_FORWARD        182  'to 182'
            162_0  COME_FROM           104  '104'

 L. 643       162  LOAD_FAST                'page_range'
              164  LOAD_METHOD              extend
              166  LOAD_GLOBAL              range
              168  LOAD_CONST               0
              170  LOAD_FAST                'page_num'
              172  LOAD_CONST               1
              174  BINARY_ADD       
              176  CALL_FUNCTION_2       2  '2 positional arguments'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  POP_TOP          
            182_0  COME_FROM           160  '160'

 L. 644       182  LOAD_FAST                'page_num'
              184  LOAD_FAST                'paginator'
              186  LOAD_ATTR                num_pages
              188  LOAD_FAST                'ON_EACH_SIDE'
              190  BINARY_SUBTRACT  
              192  LOAD_FAST                'ON_ENDS'
              194  BINARY_SUBTRACT  
              196  LOAD_CONST               1
              198  BINARY_SUBTRACT  
              200  COMPARE_OP               <
          202_204  POP_JUMP_IF_FALSE   270  'to 270'

 L. 645       206  LOAD_FAST                'page_range'
              208  LOAD_METHOD              extend

 L. 646       210  LOAD_GLOBAL              range
              212  LOAD_FAST                'page_num'
              214  LOAD_CONST               1
              216  BINARY_ADD       
              218  LOAD_FAST                'page_num'
              220  LOAD_FAST                'ON_EACH_SIDE'
              222  BINARY_ADD       
              224  LOAD_CONST               1
              226  BINARY_ADD       
              228  CALL_FUNCTION_2       2  '2 positional arguments'
              230  CALL_METHOD_1         1  '1 positional argument'
              232  POP_TOP          

 L. 647       234  LOAD_FAST                'page_range'
              236  LOAD_METHOD              append
              238  LOAD_GLOBAL              DOT
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          

 L. 648       244  LOAD_FAST                'page_range'
              246  LOAD_METHOD              extend
              248  LOAD_GLOBAL              range

 L. 649       250  LOAD_FAST                'paginator'
              252  LOAD_ATTR                num_pages
              254  LOAD_FAST                'ON_ENDS'
              256  BINARY_SUBTRACT  
              258  LOAD_FAST                'paginator'
              260  LOAD_ATTR                num_pages
              262  CALL_FUNCTION_2       2  '2 positional arguments'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  POP_TOP          
              268  JUMP_FORWARD        292  'to 292'
            270_0  COME_FROM           202  '202'

 L. 651       270  LOAD_FAST                'page_range'
              272  LOAD_METHOD              extend
              274  LOAD_GLOBAL              range
              276  LOAD_FAST                'page_num'
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  LOAD_FAST                'paginator'
              284  LOAD_ATTR                num_pages
              286  CALL_FUNCTION_2       2  '2 positional arguments'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  POP_TOP          
            292_0  COME_FROM           268  '268'
            292_1  COME_FROM            88  '88'
            292_2  COME_FROM            44  '44'

 L. 653       292  LOAD_FAST                'self'
              294  LOAD_ATTR                can_show_all
          296_298  JUMP_IF_FALSE_OR_POP   314  'to 314'
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                show_all
              304  UNARY_NOT        
          306_308  JUMP_IF_FALSE_OR_POP   314  'to 314'
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                multi_page
            314_0  COME_FROM           306  '306'
            314_1  COME_FROM           296  '296'
              314  STORE_FAST               'need_show_all_link'

 L. 655       316  LOAD_FAST                'self'

 L. 656       318  LOAD_FAST                'pagination_required'

 L. 657       320  LOAD_FAST                'need_show_all_link'
          322_324  JUMP_IF_FALSE_OR_POP   338  'to 338'
              326  LOAD_FAST                'self'
              328  LOAD_METHOD              get_query_string
              330  LOAD_GLOBAL              ALL_VAR
              332  LOAD_STR                 ''
              334  BUILD_MAP_1           1 
              336  CALL_METHOD_1         1  '1 positional argument'
            338_0  COME_FROM           322  '322'

 L. 658       338  LOAD_GLOBAL              map
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                get_page_number
              344  LOAD_FAST                'page_range'
              346  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 659       348  LOAD_GLOBAL              ALL_VAR

 L. 660       350  LOAD_CONST               1
              352  LOAD_CONST               ('cl', 'pagination_required', 'show_all_url', 'page_range', 'ALL_VAR', '1')
              354  BUILD_CONST_KEY_MAP_6     6 
              356  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `STORE_FAST' instruction at offset 34