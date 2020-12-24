# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo89/mogo/term/templatetags/terminal_tags.py
# Compiled at: 2017-12-26 07:14:55
# Size of source mod 2**32: 174 bytes
from django import template
from term.conf import COMMAND_CHANNEL
register = template.Library()

@register.simple_tag
def get_command_channel():
    return COMMAND_CHANNEL