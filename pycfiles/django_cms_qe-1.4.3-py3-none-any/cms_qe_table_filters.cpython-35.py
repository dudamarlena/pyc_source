# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_table/templatetags/cms_qe_table_filters.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 818 bytes
from django.template import Library, TemplateDoesNotExist, loader
register = Library()

@register.filter
def cms_qe_table_value(value: str) -> str:
    """
    Django template filter to customize displaying of values by their type.
    If value is of type bool, then is used template ``cms_qe/table/table_value_bool.html``.
    Every boilerplate or concrete app can customize this. When no template exists
    for given value type standard value represenation is used.
    """
    value_type = type(value).__name__
    template_name = 'cms_qe/table/table_value_{}.html'.format(value_type)
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return value
    else:
        context = {'value': value}
        return template.render(context)