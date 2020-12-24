# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/boxes/templatetags/box_filters.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 209 bytes
from django.template import Library
import tendenci.apps.boxes.utils as rc
register = Library()

@register.filter_function
def render_tags(content, arg=None):
    return rc(content, arg)