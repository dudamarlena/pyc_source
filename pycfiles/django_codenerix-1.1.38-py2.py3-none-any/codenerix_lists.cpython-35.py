# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix/templatetags/codenerix_lists.py
# Compiled at: 2017-12-18 07:03:26
# Size of source mod 2**32: 8984 bytes
from django.template import Library
from django.urls import reverse
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.utils import formats
from django.conf import settings
from codenerix.djng.angular_base import TupleErrorList
from codenerix.helpers import model_inspect
register = Library()

@register.filter
def widgetize(i):
    attrs = i.__dict__.get('field', {}).__dict__.get('widget', {}).__dict__.get('attrs', {})
    return attrs


@register.filter
def istype(i, kind):
    widget = i.field.widget
    if 'format_key' in type(widget).__dict__:
        ftype = type(widget).format_key
    else:
        ftype = None
    if kind == 'datetime':
        if ftype == 'DATETIME_INPUT_FORMATS':
            answer = 'DATETIME_INPUT_FORMATS'
        else:
            if ftype == 'DATE_INPUT_FORMATS':
                answer = 'DATE_INPUT_FORMATS'
            else:
                if ftype == 'TIME_INPUT_FORMATS':
                    answer = 'TIME_INPUT_FORMAT'
                else:
                    answer = False
    else:
        if kind == 'date2time':
            answer = 'DATE_INPUT_FORMATS'
        else:
            if kind == 'color':
                answer = ngmodel(i) == 'color'
            else:
                IOError("Unknown type '{0}' in 'istype' filter".format(kind))
    return answer


@register.filter
def addextra(attrs, attr):
    if attr:
        for at in attr:
            addattr(attrs, at)

    return attrs


@register.filter
def addattr(attrs, attr):
    attrsp = attr.split('=')
    key = attrsp[0]
    if len(attrsp) >= 2:
        value = '='.join(attrsp[1:])
    else:
        value = ''
    if key in attrs:
        if attrs[key]:
            if value:
                attrs[key] += ' {0}'.format(value)
        elif value:
            attrs[key] += value
    else:
        attrs[key] = value
    return attrs


@register.filter
def lockattr(attrs, cannot_update):
    if cannot_update:
        if 'ui-select2' in attrs:
            attrs.pop('ui-select2')
        newattrs = addattr(attrs, "readonly='readonly'")
        return addattr(newattrs, "disabled='disabled'")
    else:
        return attrs


@register.filter
def setattrs(field, attrs):
    if attrs:
        return field.as_widget(attrs=attrs)
    else:
        return field


@register.filter
def ngmodel(i):
    return getattr(i.field.widget, 'field_name', i.field.widget.attrs['ng-model'])


@register.filter
def inireadonly(attrs, i):
    field = ngmodel(i)
    return addattr(attrs, 'ng-readonly=readonly_{0}'.format(field))


@register.filter
def date2timewidget(i, langcode):
    return datewidget(i, langcode, 'date2time')


@register.filter
def datewidget(i, langcode, kindtype='datetime', kind=None):
    final = {}
    form = formats.get_format('DATETIME_INPUT_FORMATS', lang=langcode)[0].replace('%', '').replace('d', 'dd').replace('m', 'mm').replace('Y', 'yyyy').replace('H', 'hh').replace('M', 'ii').replace('S', 'ss')
    if kind is None:
        kind = istype(i, kindtype)
    if kind == 'DATETIME_INPUT_FORMATS':
        final['format'] = form
        final['startview'] = 2
        final['minview'] = 0
        final['maxview'] = 4
        final['icon'] = 'calendar'
    else:
        if kind == 'DATE_INPUT_FORMATS' or kind == 'date':
            final['format'] = form.split(' ')[0]
            final['startview'] = 2
            final['minview'] = 2
            final['maxview'] = 4
            final['icon'] = 'calendar'
        else:
            if kind == 'TIME_INPUT_FORMAT':
                final['format'] = form.split(' ')[1]
                final['startview'] = 1
                final['minview'] = 0
                final['maxview'] = 1
                final['icon'] = 'time'
            else:
                raise IOError("Unknown kind '{0}' in filter 'datewidget'".format(kind))
    return final


@register.filter
def unlist(elements):
    newtuple = TupleErrorList()
    for error in elements:
        f1, f2, f3, f4, f5, msg = error
        if type(msg) == ValidationError:
            newmsg = ''
            for error in msg:
                if newmsg:
                    newmsg += ' {0}'.format(error)
                else:
                    newmsg = error

            msg = newmsg
        newtuple.append((f1, f2, f3, f4, f5, msg))

    return newtuple


@register.filter
def foreignkey(element, exceptions):
    """
    function to determine if each select field needs a create button or not
    """
    label = element.field.__dict__['label']
    try:
        label = unicode(label)
    except NameError:
        pass

    if not label or label in exceptions:
        return False
    else:
        return '_queryset' in element.field.__dict__


@register.filter
def headstyle(group):
    style = ''
    if 'color' in group and group['color']:
        style += 'color:{0};'.format(group['color'])
    if 'bgcolor' in group and group['bgcolor']:
        style += 'background-color:{0};'.format(group['bgcolor'])
    if 'textalign' in group and group['textalign']:
        style += 'text-align:{0};'.format(group['textalign'])
    if style:
        return 'style={0}'.format(style)
    else:
        return ''


class ColumnCounter:

    def __init__(self):
        self._ColumnCounter__columns = 0

    def add(self, columns):
        if self._ColumnCounter__columns == 12:
            self._ColumnCounter__columns = 0
            answer = True
        else:
            if self._ColumnCounter__columns > 12:
                raise IOError("Columns max number of 12 reached, you requested to use a total of '{}'".format(self._ColumnCounter__columns))
            else:
                answer = False
        self._ColumnCounter__columns += columns
        return answer


@register.filter
def column_counter(nothing):
    return ColumnCounter()


@register.filter
def add_columns(obj, columns):
    return obj.add(columns)


@register.filter
def linkedinfo(element, info_input={}):
    info = model_inspect(element.field._get_queryset().model())
    info.update(info_input)
    ngmodel = element.html_name
    return mark_safe("'{0}','{1}','{2}', '{3}s'".format(getattr(settings, 'BASE_URL', ''), ngmodel, info['appname'], info['modelname'].lower()))


@register.filter
def get_depa(queryset, kind):
    return queryset.get(kind=kind, alternative=False)


@register.filter
def getws(form, input_name):
    if 'autofill' in form.Meta.__dict__ and input_name in form.Meta.autofill:
        return "'{}'".format(reverse(form.Meta.autofill[input_name][2], kwargs={'search': '__pk__'}))
    else:
        return 'undefined'


@register.filter
def get_field_list(forms):
    inputs = []
    for form in forms:
        for field in form.fields:
            inputs.append("'{}'".format(field))

    if inputs:
        inputs = '[{}]'.format(','.join(inputs))
    return inputs


@register.filter
def invalidator(formname, inp):
    return mark_safe("{{'codenerix_invalid':{0}.{1}.$invalid}}".format(smart_text(formname), ngmodel(inp)))


@register.filter
def join_list(l, string):
    if l:
        return string.join(l)
    else:
        return ''