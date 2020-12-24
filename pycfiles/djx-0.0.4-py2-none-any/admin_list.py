# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/admin/templatetags/admin_list.py
# Compiled at: 2019-02-14 00:35:15
from __future__ import unicode_literals
import datetime, warnings
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import display_for_field, display_for_value, get_fields_from_path, label_for_field, lookup_field
from django.contrib.admin.views.main import ALL_VAR, ORDER_VAR, PAGE_VAR, SEARCH_VAR
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template import Library
from django.template.loader import get_template
from django.templatetags.static import static
from django.urls import NoReverseMatch
from django.utils import formats
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
register = Library()
DOT = b'.'

@register.simple_tag
def paginator_number(cl, i):
    """
    Generates an individual page index link in a paginated list.
    """
    if i == DOT:
        return b'... '
    else:
        if i == cl.page_num:
            return format_html(b'<span class="this-page">{}</span> ', i + 1)
        return format_html(b'<a href="{}"{}>{}</a> ', cl.get_query_string({PAGE_VAR: i}), mark_safe(b' class="end"' if i == cl.paginator.num_pages - 1 else b''), i + 1)


@register.inclusion_tag(b'admin/pagination.html')
def pagination(cl):
    """
    Generates the series of links to the pages in a paginated list.
    """
    paginator, page_num = cl.paginator, cl.page_num
    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2
        if paginator.num_pages <= 10:
            page_range = range(paginator.num_pages)
        else:
            page_range = []
            if page_num > ON_EACH_SIDE + ON_ENDS:
                page_range.extend(range(0, ON_ENDS))
                page_range.append(DOT)
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1:
                page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.append(DOT)
                page_range.extend(range(paginator.num_pages - ON_ENDS, paginator.num_pages))
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))
    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return {b'cl': cl, 
       b'pagination_required': pagination_required, 
       b'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: b''}), 
       b'page_range': page_range, 
       b'ALL_VAR': ALL_VAR, 
       b'1': 1}


def result_headers(cl):
    """
    Generates the list column headers.
    """
    ordering_field_columns = cl.get_ordering_field_columns()
    for i, field_name in enumerate(cl.list_display):
        text, attr = label_for_field(field_name, cl.model, model_admin=cl.model_admin, return_attr=True)
        if attr:
            field_name = _coerce_field_name(field_name, i)
            if field_name == b'action_checkbox':
                yield {b'text': text, b'class_attrib': mark_safe(b' class="action-checkbox-column"'), 
                   b'sortable': False}
                continue
            admin_order_field = getattr(attr, b'admin_order_field', None)
            if not admin_order_field:
                yield {b'text': text, 
                   b'class_attrib': format_html(b' class="column-{}"', field_name), 
                   b'sortable': False}
                continue
        th_classes = [
         b'sortable', (b'column-{}').format(field_name)]
        order_type = b''
        new_order_type = b'asc'
        sort_priority = 0
        sorted = False
        if i in ordering_field_columns:
            sorted = True
            order_type = ordering_field_columns.get(i).lower()
            sort_priority = list(ordering_field_columns).index(i) + 1
            th_classes.append(b'sorted %sending' % order_type)
            new_order_type = {b'asc': b'desc', b'desc': b'asc'}[order_type]
        o_list_primary = []
        o_list_remove = []
        o_list_toggle = []

        def make_qs_param(t, n):
            return (b'-' if t == b'desc' else b'') + str(n)

        for j, ot in ordering_field_columns.items():
            if j == i:
                param = make_qs_param(new_order_type, j)
                o_list_primary.insert(0, param)
                o_list_toggle.append(param)
            else:
                param = make_qs_param(ot, j)
                o_list_primary.append(param)
                o_list_toggle.append(param)
                o_list_remove.append(param)

        if i not in ordering_field_columns:
            o_list_primary.insert(0, make_qs_param(new_order_type, i))
        yield {b'text': text, 
           b'sortable': True, 
           b'sorted': sorted, 
           b'ascending': order_type == b'asc', 
           b'sort_priority': sort_priority, 
           b'url_primary': cl.get_query_string({ORDER_VAR: (b'.').join(o_list_primary)}), 
           b'url_remove': cl.get_query_string({ORDER_VAR: (b'.').join(o_list_remove)}), 
           b'url_toggle': cl.get_query_string({ORDER_VAR: (b'.').join(o_list_toggle)}), 
           b'class_attrib': format_html(b' class="{}"', (b' ').join(th_classes)) if th_classes else b''}

    return


def _boolean_icon(field_val):
    icon_url = static(b'admin/img/icon-%s.svg' % {True: b'yes', False: b'no', None: b'unknown'}[field_val])
    return format_html(b'<img src="{}" alt="{}" />', icon_url, field_val)


def _coerce_field_name(field_name, field_index):
    """
    Coerce a field_name (which may be a callable) to a string.
    """
    if callable(field_name):
        if field_name.__name__ == b'<lambda>':
            return b'lambda' + str(field_index)
        else:
            return field_name.__name__

    return field_name


def items_for_result(cl, result, form):
    """
    Generates the actual list of data.
    """

    def link_in_col(is_first, field_name, cl):
        if cl.list_display_links is None:
            return False
        else:
            if is_first and not cl.list_display_links:
                return True
            return field_name in cl.list_display_links

    first = True
    pk = cl.lookup_opts.pk.attname
    for field_index, field_name in enumerate(cl.list_display):
        empty_value_display = cl.model_admin.get_empty_value_display()
        row_classes = [b'field-%s' % _coerce_field_name(field_name, field_index)]
        try:
            f, attr, value = lookup_field(field_name, result, cl.model_admin)
        except ObjectDoesNotExist:
            result_repr = empty_value_display
        else:
            empty_value_display = getattr(attr, b'empty_value_display', empty_value_display)
            if f is None or f.auto_created:
                if field_name == b'action_checkbox':
                    row_classes = [
                     b'action-checkbox']
                allow_tags = getattr(attr, b'allow_tags', False)
                boolean = getattr(attr, b'boolean', False)
                result_repr = display_for_value(value, empty_value_display, boolean)
                if allow_tags:
                    warnings.warn((b'Deprecated allow_tags attribute used on field {}. Use django.utils.html.format_html(), format_html_join(), or django.utils.safestring.mark_safe() instead.').format(field_name), RemovedInDjango20Warning)
                    result_repr = mark_safe(result_repr)
                if isinstance(value, (datetime.date, datetime.time)):
                    row_classes.append(b'nowrap')
            else:
                if isinstance(f.remote_field, models.ManyToOneRel):
                    field_val = getattr(result, f.name)
                    if field_val is None:
                        result_repr = empty_value_display
                    else:
                        result_repr = field_val
                else:
                    result_repr = display_for_field(value, f, empty_value_display)
                if isinstance(f, (models.DateField, models.TimeField, models.ForeignKey)):
                    row_classes.append(b'nowrap')
            if force_text(result_repr) == b'':
                result_repr = mark_safe(b'&nbsp;')
            row_class = mark_safe(b' class="%s"' % (b' ').join(row_classes))
            if link_in_col(first, field_name, cl):
                table_tag = b'th' if first else b'td'
                first = False
                try:
                    url = cl.url_for_result(result)
                except NoReverseMatch:
                    link_or_text = result_repr
                else:
                    url = add_preserved_filters({b'preserved_filters': cl.preserved_filters, b'opts': cl.opts}, url)
                    if cl.to_field:
                        attr = str(cl.to_field)
                    else:
                        attr = pk
                    value = result.serializable_value(attr)
                    link_or_text = format_html(b'<a href="{}"{}>{}</a>', url, format_html(b' data-popup-opener="{}"', value) if cl.is_popup else b'', result_repr)

                yield format_html(b'<{}{}>{}</{}>', table_tag, row_class, link_or_text, table_tag)
            else:
                if form and field_name in form.fields and not (field_name == cl.model._meta.pk.name and form[cl.model._meta.pk.name].is_hidden):
                    bf = form[field_name]
                    result_repr = mark_safe(force_text(bf.errors) + force_text(bf))
                yield format_html(b'<td{}>{}</td>', row_class, result_repr)

    if form and not form[cl.model._meta.pk.name].is_hidden:
        yield format_html(b'<td>{}</td>', force_text(form[cl.model._meta.pk.name]))
    return


class ResultList(list):

    def __init__(self, form, *items):
        self.form = form
        super(ResultList, self).__init__(*items)


def results(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield ResultList(form, items_for_result(cl, res, form))

    else:
        for res in cl.result_list:
            yield ResultList(None, items_for_result(cl, res, None))

    return


def result_hidden_fields(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            if form[cl.model._meta.pk.name].is_hidden:
                yield mark_safe(force_text(form[cl.model._meta.pk.name]))


@register.inclusion_tag(b'admin/change_list_results.html')
def result_list(cl):
    """
    Displays the headers and data list together
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h[b'sortable'] and h[b'sorted']:
            num_sorted_fields += 1

    return {b'cl': cl, b'result_hidden_fields': list(result_hidden_fields(cl)), 
       b'result_headers': headers, 
       b'num_sorted_fields': num_sorted_fields, 
       b'results': list(results(cl))}


@register.inclusion_tag(b'admin/date_hierarchy.html')
def date_hierarchy(cl):
    """
    Displays the date hierarchy for date drill-down functionality.
    """
    if cl.date_hierarchy:
        field_name = cl.date_hierarchy
        field = get_fields_from_path(cl.model, field_name)[(-1)]
        dates_or_datetimes = b'datetimes' if isinstance(field, models.DateTimeField) else b'dates'
        year_field = b'%s__year' % field_name
        month_field = b'%s__month' % field_name
        day_field = b'%s__day' % field_name
        field_generic = b'%s__' % field_name
        year_lookup = cl.params.get(year_field)
        month_lookup = cl.params.get(month_field)
        day_lookup = cl.params.get(day_field)

        def link(filters):
            return cl.get_query_string(filters, [field_generic])

        if not (year_lookup or month_lookup or day_lookup):
            date_range = cl.queryset.aggregate(first=models.Min(field_name), last=models.Max(field_name))
            if date_range[b'first'] and date_range[b'last']:
                if date_range[b'first'].year == date_range[b'last'].year:
                    year_lookup = date_range[b'first'].year
                    if date_range[b'first'].month == date_range[b'last'].month:
                        month_lookup = date_range[b'first'].month
        if year_lookup and month_lookup and day_lookup:
            day = datetime.date(int(year_lookup), int(month_lookup), int(day_lookup))
            return {b'show': True, 
               b'back': {b'link': link({year_field: year_lookup, month_field: month_lookup}), 
                         b'title': capfirst(formats.date_format(day, b'YEAR_MONTH_FORMAT'))}, 
               b'choices': [{b'title': capfirst(formats.date_format(day, b'MONTH_DAY_FORMAT'))}]}
        if year_lookup and month_lookup:
            days = cl.queryset.filter(**{year_field: year_lookup, month_field: month_lookup})
            days = getattr(days, dates_or_datetimes)(field_name, b'day')
            return {b'show': True, 
               b'back': {b'link': link({year_field: year_lookup}), 
                         b'title': str(year_lookup)}, 
               b'choices': [ {b'link': link({year_field: year_lookup, month_field: month_lookup, day_field: day.day}), b'title': capfirst(formats.date_format(day, b'MONTH_DAY_FORMAT'))} for day in days
                         ]}
        if year_lookup:
            months = cl.queryset.filter(**{year_field: year_lookup})
            months = getattr(months, dates_or_datetimes)(field_name, b'month')
            return {b'show': True, 
               b'back': {b'link': link({}), 
                         b'title': _(b'All dates')}, 
               b'choices': [ {b'link': link({year_field: year_lookup, month_field: month.month}), b'title': capfirst(formats.date_format(month, b'YEAR_MONTH_FORMAT'))} for month in months
                         ]}
        years = getattr(cl.queryset, dates_or_datetimes)(field_name, b'year')
        return {b'show': True, 
           b'choices': [ {b'link': link({year_field: str(year.year)}), b'title': str(year.year)} for year in years
                     ]}


@register.inclusion_tag(b'admin/search_form.html')
def search_form(cl):
    """
    Displays a search form for searching the list.
    """
    return {b'cl': cl, 
       b'show_result_count': cl.result_count != cl.full_result_count, 
       b'search_var': SEARCH_VAR}


@register.simple_tag
def admin_list_filter(cl, spec):
    tpl = get_template(spec.template)
    return tpl.render({b'title': spec.title, 
       b'choices': list(spec.choices(cl)), 
       b'spec': spec})


@register.inclusion_tag(b'admin/actions.html', takes_context=True)
def admin_actions(context):
    """
    Track the number of times the action field has been rendered on the page,
    so we know which value to use.
    """
    context[b'action_index'] = context.get(b'action_index', -1) + 1
    return context