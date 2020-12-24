# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/irakli/Documents/python/projects/test_d/django_phonenumbers/templatetags/phone_numbers_extra.py
# Compiled at: 2015-07-23 14:14:21
# Size of source mod 2**32: 2564 bytes
from django import template
from django.conf import settings
from phonenumbers import NumberFormat
import phonenumbers
from django_phonenumbers.helper import PhoneNumber
register = template.Library()

@register.filter()
def phone_number_format(number, region_code=None):
    if type(number) is str:
        if region_code is None:
            return number
        new_number = phonenumbers.parse(number, region_code)
    else:
        if type(number) is PhoneNumber:
            region_code = number.region_code
            new_number = phonenumbers.parse(number.phone_number, number.region_code)
        else:
            return ''
    if hasattr(settings, 'PHONE_NUMBERS_FORMATS_BY_REGION'):
        region_pattern = settings.PHONE_NUMBERS_FORMATS_BY_REGION.get(region_code, None)
        if region_pattern is None:
            phonenumbers.format_number(new_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        else:
            try:
                new_number_format = NumberFormat(pattern=region_pattern.get('pattern'), format=region_pattern.get('format'))
                new_number_format._mutable = True
                new_number_format.national_prefix_formatting_rule = region_pattern.get('prefix_format') % (
                 new_number.country_code, '$FG')
                new_number_formats = [
                 new_number_format]
                return phonenumbers.format_by_pattern(new_number, phonenumbers.PhoneNumberFormat.NATIONAL, new_number_formats)
            except:
                return number

    return number


@register.simple_tag()
def phone_number(number, pattern=None, number_format=None, region_code=None, prefix_format=None):
    r"""
        for number +995595119925
        pattern="(\d{3})(\d{2})(\d{2})(\d{2})", format="\1 \2-\3-\4"
        result 595 11-99-25
    """
    if type(number) is str:
        number = phonenumbers.parse(number, region_code)
    else:
        if type(number) is PhoneNumber:
            number = phonenumbers.parse(number.phone_number, number.region_code)
        else:
            return ''
    new_number_format = NumberFormat(pattern=pattern, format=number_format)
    new_number_format._mutable = True
    new_number_format.national_prefix_formatting_rule = prefix_format % (number.country_code, '$FG')
    new_number_formats = [new_number_format]
    return phonenumbers.format_by_pattern(number, phonenumbers.PhoneNumberFormat.NATIONAL, new_number_formats)