# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alex/projects/pip_packages/qnc_crud/qnc_crud/templatetags/phone_link.py
# Compiled at: 2020-03-10 14:42:03
# Size of source mod 2**32: 1067 bytes
import re
from django import template
from django.utils.html import format_html
register = template.Library()

def international_format(possible_phone_number, default_area_code='306'):
    possible_phone_number = possible_phone_number.lower().split('x')[0]
    digits = re.sub('\\D', '', possible_phone_number)
    if len(digits) == 7:
        digits = default_area_code + digits
    if len(digits) == 10:
        digits = '1' + digits
    if len(digits) != 11:
        return
    else:
        return '+' + digits


@register.filter
def possible_phone_href(possible_phone_number):
    """
        Suggested Usage:
            <a {{some_number|possible_phone_href}}>{{possible_phone_number}}</a>

        You always have the wrapping <a>, even if we can't parse the number.
        If we can't parse the number, no href is printed (which is valid html, a tag will NOT match :link)
    """
    n = international_format(possible_phone_number)
    if not n:
        return ''
    else:
        return format_html(' href="tel:{}"', n)