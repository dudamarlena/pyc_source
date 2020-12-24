# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/base/templatetags/admin_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 618 bytes
from django.template import Library
from tendenci.apps.site_settings.utils import get_setting
register = Library()

@register.filter
def check_enabled(value):
    return get_setting('module', value.lower(), 'enabled') is not False


@register.filter(name='tadmin_form_line_column_width')
def tadmin_form_line_column_width(line):
    try:
        width = len(list(line))
        value = 12 // width
        return value
    except:
        return 12