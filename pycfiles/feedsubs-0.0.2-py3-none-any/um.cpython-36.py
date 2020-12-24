# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/um/templatetags/um.py
# Compiled at: 2018-12-13 14:13:37
# Size of source mod 2**32: 383 bytes
from django import template
from ..background_messages import add_background_messages_to_contrib_messages
register = template.Library()

@register.simple_tag(takes_context=True)
def fetch_background_messages(context):
    """Template tag adding background messages to contrib message framework."""
    add_background_messages_to_contrib_messages(context['request'])
    return ''