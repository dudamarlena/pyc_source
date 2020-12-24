# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/numberformat.py
# Compiled at: 2018-07-11 18:15:30
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils import six

def format(number, decimal_sep, decimal_pos=None, grouping=0, thousand_sep='', force_grouping=False):
    """
    Gets a number (as a number or string), and returns it as a string,
    using formats defined as arguments:

    * decimal_sep: Decimal separator symbol (for example ".")
    * decimal_pos: Number of decimal positions
    * grouping: Number of digits in every group limited by thousand separator
    * thousand_sep: Thousand separator symbol (for example ",")
    """
    use_grouping = settings.USE_L10N and settings.USE_THOUSAND_SEPARATOR
    use_grouping = use_grouping or force_grouping
    use_grouping = use_grouping and grouping > 0
    if isinstance(number, int) and not use_grouping and not decimal_pos:
        return mark_safe(six.text_type(number))
    else:
        sign = ''
        str_number = six.text_type(number)
        if str_number[0] == '-':
            sign = '-'
            str_number = str_number[1:]
        if '.' in str_number:
            int_part, dec_part = str_number.split('.')
            if decimal_pos is not None:
                dec_part = dec_part[:decimal_pos]
        else:
            int_part, dec_part = str_number, ''
        if decimal_pos is not None:
            dec_part = dec_part + '0' * (decimal_pos - len(dec_part))
        if dec_part:
            dec_part = decimal_sep + dec_part
        if use_grouping:
            int_part_gd = ''
            for cnt, digit in enumerate(int_part[::-1]):
                if cnt and not cnt % grouping:
                    int_part_gd += thousand_sep
                int_part_gd += digit

            int_part = int_part_gd[::-1]
        return sign + int_part + dec_part