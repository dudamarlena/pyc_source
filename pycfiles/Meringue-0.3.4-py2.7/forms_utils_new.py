# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/templatetags/forms_utils_new.py
# Compiled at: 2015-08-22 16:34:49
import logging, re
from bs4 import BeautifulSoup
from django import forms
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

def get_name(field):
    caption = field.widget.__class__.__name__
    r = '([A-Z]{1})([a-z]+)'
    p = re.compile(r)
    caption = p.sub(lambda m: '_' + m.group().lower(), caption)
    return caption


@register.filter
def field_render_classes(boundfield):
    u"""
        выводит список параметров через пробел
            required - если обязательное поле
            errors - если есть ошибки
            valid - если валидное
            meringue-<field_name> - идентификатор
    """
    result = ''
    if boundfield.field.required:
        result += ' required'
    if boundfield.errors:
        result += ' errors'
    if not boundfield.errors and boundfield.form.errors and boundfield.value:
        result += ' valid'
    result += ' meringue-' + get_name(boundfield.field)[1:]
    return result


class FieldRender(object):

    def __init__(self, boundfield):
        self.field = boundfield
        self.caption = get_name(boundfield.field)

    def render(self):
        result = getattr(self, self.caption + '_render', self._default_with_label_render)
        return result()

    def _default_with_label_render(self):
        result = '<label for="id_%s" >%s</label>%s' % (
         self.field.html_name,
         unicode(self.field.label),
         self.field)
        return mark_safe(result)


@register.filter
def field_render(boundfield):
    u"""
        Рендерит поле в соответствии с правилами
    """
    result = FieldRender(boundfield)
    return result.render()


register = template.Library()

@register.filter
def add_placeholder(field):
    u"""
        Устанавливает placeholder равный значению label
    """
    soup = BeautifulSoup(unicode(field), 'html.parser')
    for tag in soup.children:
        if tag.name != 'script':
            tag['placeholder'] = field.label

    return mark_safe(soup.renderContents())