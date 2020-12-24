# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcos/rapid-django/src/rapid/filters.py
# Compiled at: 2015-09-18 17:15:35
__author__ = 'marcos.medeiros'
from django.db import models
from django.db.models.fields.related import ForeignObjectRel
import datetime, decimal, inspect, locale
from django.template import loader, Context
_filter_templates = 'rapid/filters/'
_filter_url_parameter = 'filter'

class FilterOperator:

    def __init__(self, display, query, multiple=False):
        self.display = display
        self.query = query
        self.multiple = multiple


class FilterValue:
    available_operations = []
    selection_template = _filter_templates + 'key_value.html'

    def __init__(self, field, url_value=''):
        self.value = None
        self.field = field
        raise NotImplementedError
        return

    def query_value(self):
        return self.value

    def url_value(self):
        return unicode(self.value)

    def operator_from_url(self, url_value):
        for o in self.available_operations:
            if unicode(o.query) == unicode(url_value):
                return o

        return


class IntegralFilter(FilterValue):
    available_operations = [
     FilterOperator('igual a', 'exact'),
     FilterOperator('maior que', 'gt'),
     FilterOperator('maior ou igual a', 'gte'),
     FilterOperator('menor que', 'lt'),
     FilterOperator('menor ou igual a', 'lte')]

    def __init__(self, field, url_value=0):
        self.value = int(url_value)


class BooleanFilter(FilterValue):
    available_operations = [
     FilterOperator('valor', 'exact')]

    def __init__(self, field, url_value='true'):
        self.value = bool(url_value)

    def __unicode__(self):
        if self.value:
            return 'true'
        return ''


class TextFilter(FilterValue):
    available_operations = [
     FilterOperator('igual a', 'iexact'),
     FilterOperator('começa com', 'istartswith'),
     FilterOperator('acaba com', 'iendswith'),
     FilterOperator('contém', 'icontains')]

    def __init__(self, field, url_value=''):
        self.value = url_value

    def url_value(self):
        if self.value:
            return self.value
        return ''


class DateTimeFilter(FilterValue):
    selection_template = _filter_templates + 'date_value.html'
    available_operations = [
     FilterOperator('igual a', 'exact'),
     FilterOperator('maior que', 'gt'),
     FilterOperator('maior ou igual a', 'gte'),
     FilterOperator('menor que', 'lt'),
     FilterOperator('menor ou igual a', 'lte')]
    dateformat = '%Y:%m:%d:%H:%M:%S'

    def __init__(self, field, url_value=None):
        if url_value:
            self.value = datetime.datetime.strptime(url_value, self.dateformat)
        else:
            self.value = datetime.datetime.now()

    def url_value(self):
        return self.value.strftime(self.dateformat)


class RealFilter(FilterValue):
    available_operations = [
     FilterOperator('igual a', 'exact'),
     FilterOperator('maior que', 'gt'),
     FilterOperator('maior ou igual a', 'gte'),
     FilterOperator('menor que', 'lt'),
     FilterOperator('menor ou igual a', 'lte')]

    def __init__(self, field, url_value=0.0):
        self.value = decimal.Decimal(url_value)


class TimeFilter(DateTimeFilter):
    available_operations = [
     FilterOperator('igual a', 'exact'),
     FilterOperator('maior que', 'gt'),
     FilterOperator('maior ou igual a', 'gte'),
     FilterOperator('menor que', 'lt'),
     FilterOperator('menor ou igual a', 'lte')]
    dateformat = 'HH:MM:SS'


class RelationFilter(FilterValue):
    available_operations = [
     FilterOperator('igual a', 'exact'),
     FilterOperator('na lista', 'in')]

    def __init__(self, field, url_value=''):
        model = field.related_model()
        self.model = model
        self.value = [ model.default_manager().filter(pk__in=int(v)) for v in url_value.split(':') if v ]

    def url_value(self):
        return (':').join([ str(v.pk) for v in self.value ])


field_type_dispatcher = {models.AutoField: IntegralFilter, 
   models.BigIntegerField: IntegralFilter, 
   models.CharField: TextFilter, 
   models.EmailField: TextFilter, 
   models.FloatField: RealFilter, 
   models.IntegerField: IntegralFilter, 
   models.PositiveIntegerField: IntegralFilter, 
   models.PositiveSmallIntegerField: IntegralFilter, 
   models.SmallIntegerField: IntegralFilter, 
   models.TextField: TextFilter}

def _get_field_type(field):
    tt = inspect.getmro(type(field.field))
    for t in tt:
        v = field_type_dispatcher.get(t)
        if v:
            return v

    return


def _get_default_field_value(field):
    t = _get_field_type(field)
    if t:
        return t(field)
    else:
        return


def _get_field_value(field, url_value):
    value_type = _get_field_type(field)
    if value_type:
        return value_type(field, url_value)
    else:
        return


class Filter:

    def __init__(self, field, operator=None, value=None):
        self.field = field
        if value:
            self.value = value
        else:
            self.value = _get_default_field_value(field)
        if operator:
            self.operator = operator
        else:
            self.operator = self.value.available_operations[0]

    def query_dict(self):
        return (self.field.bare_name() + '__' + self.operator.query, self.value.query_value())

    def url_para(self):
        return self.field.bare_name() + '-' + self.operator.query + '=' + self.value.url_vaue()

    @classmethod
    def from_request(cls, field, request):
        for o in _get_field_type(field).available_operations:
            if request.GET.has_key(field.bare_name() + '-' + o.query):
                valstr = request.GET[(field.bare_name() + '-' + o.query)]
                val = _get_field_value(field, valstr)
                yield Filter(field, o, val)

    def selection_value_html(self, request):
        c = Context({'id': self.field.bare_name() + '_' + self.operator.query, 
           'field': self.field, 
           'operator': self.operator, 
           'default_value': self.value.value})
        t = loader.get_template(self.value.selection_template)
        return t.render(c, request)

    @classmethod
    def selection_type_html(cls, field, request):
        v = _get_field_type(field)
        ff = [ Filter(field, o) for o in v.available_operations ]
        ss = [ (f.operator, f.selection_value_html(request)) for f in ff ]
        act = request.get_full_path()
        c = Context({'field': field, 
           'operators': v.available_operations, 
           'selectors': ss, 
           'action': act})
        t = loader.get_template(_filter_templates + 'column_selector.html')
        return t.render(c)


class FilterSet:

    def __init__(self, filters=None):
        self.filters = filters if filters else {}

    def query_dict(self):
        q = []
        for ff in self.filters.values():
            q += [ f.query_dict() for f in ff ]

        return dict(q)

    def url_para(self):
        return (';').join([ f.url_para for f in self.filters ])

    @classmethod
    def from_request(cls, model, request):
        ff = dict([ (f, list(Filter.from_request(f, request))) for f in model.fields() if _get_field_type(f) ])
        return FilterSet(ff)

    @classmethod
    def can_filter(cls, field):
        return bool(_get_field_type(field))

    def render_filters(self, request):
        remove_filter_element = '<a class="rapid-remove-filter"><span class="fa fa-times"></span></a>'
        ret = ''
        kk = self.filters.keys()
        kk.sort(key=lambda f: f.name(), cmp=locale.strcoll)
        for field in kk:
            ret += '<div class="rapid-field-filters %s %s">%s\n' % ('visible' if self.filters[field] else 'hidden',
             field.bare_name(), field.name().capitalize())
            for f in self.filters[field]:
                ret += '<div>' + f.selection_value_html(request) + remove_filter_element + '</div>\n'

            ret += '</div>'

        return ret

    def render_selectors(self, request):
        ret = ''
        kk = self.filters.keys()
        kk.sort(key=lambda f: f.name(), cmp=locale.strcoll)
        for field in kk:
            ret += '<div class="rapid-filter-selection %s hidden">\n' % field.bare_name()
            ret += Filter.selection_type_html(field, request)
            ret += '</div>\n'

        return ret

    def filters_url(self):
        pass

    def has_filters(self):
        for k in self.filters.keys():
            if self.filters[k]:
                return True

        return False