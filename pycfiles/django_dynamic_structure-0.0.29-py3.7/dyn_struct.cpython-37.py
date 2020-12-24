# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/templatetags/dyn_struct.py
# Compiled at: 2016-09-07 04:46:55
# Size of source mod 2**32: 483 bytes
import six, json, django.template
register = django.template.Library()

@register.inclusion_tag('dyn_struct/render_struct.html')
def render_struct(structure_obj, prefix, value=None, template='bootstrap3'):
    if value:
        if isinstance(value, six.string_types):
            value = json.loads(value)
    form = structure_obj.build_form(data=value, prefix=prefix)
    rows = structure_obj.get_rows(form)
    return {'rows':rows, 
     'template':template}