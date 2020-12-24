# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/syn/dev/test/mogo76/mogo/spages/templatetags/spages_tags.py
# Compiled at: 2016-11-01 04:48:08
from django import template
from spages.conf import CODE_MODE
register = template.Library()

@register.simple_tag
def get_edit_mode():
    if CODE_MODE == True:
        return 'code'
    else:
        return 'default'