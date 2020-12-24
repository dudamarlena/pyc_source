# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/email_blocks/templatetags/email_block_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 462 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('email_blocks/options.html', takes_context=True)
def email_block_options(context, email_block):
    context.update({'opt_object': email_block})
    return context


@register.inclusion_tag('email_blocks/nav.html', takes_context=True)
def email_blocks_nav(context, email_block=None):
    context.update({'nav_object': email_block})
    return context