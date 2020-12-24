# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo64/mogo/dex/templatetags/dex_tags.py
# Compiled at: 2017-08-04 08:23:46
# Size of source mod 2**32: 173 bytes
from django import template
from dex.conf import COMMAND_CHANNEL
register = template.Library()

@register.simple_tag
def get_command_channel():
    return COMMAND_CHANNEL