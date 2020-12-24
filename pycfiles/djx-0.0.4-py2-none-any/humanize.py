# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/humanize/templatetags/humanize.py
# Compiled at: 2019-02-14 00:35:16
from __future__ import unicode_literals
import re
from datetime import date, datetime
from decimal import Decimal
from django import template
from django.conf import settings
from django.template import defaultfilters
from django.utils.encoding import force_text
from django.utils.formats import number_format
from django.utils.safestring import mark_safe
from django.utils.timezone import is_aware, utc
from django.utils.translation import pgettext, ugettext as _, ungettext
register = template.Library()

@register.filter(is_safe=True)
def ordinal(value):
    """
    Converts an integer to its ordinal as a string. 1 is '1st', 2 is '2nd',
    3 is '3rd', etc. Works for any integer.
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    suffixes = (
     _(b'th'), _(b'st'), _(b'nd'), _(b'rd'), _(b'th'), _(b'th'), _(b'th'), _(b'th'), _(b'th'), _(b'th'))
    if value % 100 in (11, 12, 13):
        return mark_safe(b'%d%s' % (value, suffixes[0]))
    return mark_safe(b'%d%s' % (value, suffixes[(value % 10)]))


@register.filter(is_safe=True)
def intcomma(value, use_l10n=True):
    """
    Converts an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    if settings.USE_L10N and use_l10n:
        try:
            if not isinstance(value, (float, Decimal)):
                value = int(value)
        except (TypeError, ValueError):
            return intcomma(value, False)

        return number_format(value, force_grouping=True)
    orig = force_text(value)
    new = re.sub(b'^(-?\\d+)(\\d{3})', b'\\g<1>,\\g<2>', orig)
    if orig == new:
        return new
    else:
        return intcomma(new, use_l10n)


intword_converters = (
 (
  6,
  lambda number: (
   ungettext(b'%(value).1f million', b'%(value).1f million', number),
   ungettext(b'%(value)s million', b'%(value)s million', number))),
 (
  9,
  lambda number: (
   ungettext(b'%(value).1f billion', b'%(value).1f billion', number),
   ungettext(b'%(value)s billion', b'%(value)s billion', number))),
 (
  12,
  lambda number: (
   ungettext(b'%(value).1f trillion', b'%(value).1f trillion', number),
   ungettext(b'%(value)s trillion', b'%(value)s trillion', number))),
 (
  15,
  lambda number: (
   ungettext(b'%(value).1f quadrillion', b'%(value).1f quadrillion', number),
   ungettext(b'%(value)s quadrillion', b'%(value)s quadrillion', number))),
 (
  18,
  lambda number: (
   ungettext(b'%(value).1f quintillion', b'%(value).1f quintillion', number),
   ungettext(b'%(value)s quintillion', b'%(value)s quintillion', number))),
 (
  21,
  lambda number: (
   ungettext(b'%(value).1f sextillion', b'%(value).1f sextillion', number),
   ungettext(b'%(value)s sextillion', b'%(value)s sextillion', number))),
 (
  24,
  lambda number: (
   ungettext(b'%(value).1f septillion', b'%(value).1f septillion', number),
   ungettext(b'%(value)s septillion', b'%(value)s septillion', number))),
 (
  27,
  lambda number: (
   ungettext(b'%(value).1f octillion', b'%(value).1f octillion', number),
   ungettext(b'%(value)s octillion', b'%(value)s octillion', number))),
 (
  30,
  lambda number: (
   ungettext(b'%(value).1f nonillion', b'%(value).1f nonillion', number),
   ungettext(b'%(value)s nonillion', b'%(value)s nonillion', number))),
 (
  33,
  lambda number: (
   ungettext(b'%(value).1f decillion', b'%(value).1f decillion', number),
   ungettext(b'%(value)s decillion', b'%(value)s decillion', number))),
 (
  100,
  lambda number: (
   ungettext(b'%(value).1f googol', b'%(value).1f googol', number),
   ungettext(b'%(value)s googol', b'%(value)s googol', number))))

@register.filter(is_safe=False)
def intword(value):
    """
    Converts a large integer to a friendly text representation. Works best
    for numbers over 1 million. For example, 1000000 becomes '1.0 million',
    1200000 becomes '1.2 million' and '1200000000' becomes '1.2 billion'.
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < 1000000:
        return value

    def _check_for_i18n(value, float_formatted, string_formatted):
        """
        Use the i18n enabled defaultfilters.floatformat if possible
        """
        if settings.USE_L10N:
            value = defaultfilters.floatformat(value, 1)
            template = string_formatted
        else:
            template = float_formatted
        return template % {b'value': value}

    for exponent, converters in intword_converters:
        large_number = 10 ** exponent
        if value < large_number * 1000:
            new_value = value / float(large_number)
            return _check_for_i18n(new_value, *converters(new_value))

    return value


@register.filter(is_safe=True)
def apnumber(value):
    """
    For numbers 1-9, returns the number spelled out. Otherwise, returns the
    number. This follows Associated Press style.
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if not 0 < value < 10:
        return value
    return (
     _(b'one'), _(b'two'), _(b'three'), _(b'four'), _(b'five'),
     _(b'six'), _(b'seven'), _(b'eight'), _(b'nine'))[(value - 1)]


@register.filter(expects_localtime=True)
def naturalday(value, arg=None):
    """
    For date values that are tomorrow, today or yesterday compared to
    present day returns representing string. Otherwise, returns a string
    formatted according to settings.DATE_FORMAT.
    """
    try:
        tzinfo = getattr(value, b'tzinfo', None)
        value = date(value.year, value.month, value.day)
    except AttributeError:
        return value
    except ValueError:
        return value

    today = datetime.now(tzinfo).date()
    delta = value - today
    if delta.days == 0:
        return _(b'today')
    else:
        if delta.days == 1:
            return _(b'tomorrow')
        if delta.days == -1:
            return _(b'yesterday')
        return defaultfilters.date(value, arg)


@register.filter
def naturaltime(value):
    """
    For date and time values shows how many seconds, minutes or hours ago
    compared to current timestamp returns representing string.
    """
    if not isinstance(value, date):
        return value
    else:
        now = datetime.now(utc if is_aware(value) else None)
        if value < now:
            delta = now - value
            if delta.days != 0:
                return pgettext(b'naturaltime', b'%(delta)s ago') % {b'delta': defaultfilters.timesince(value, now)}
            if delta.seconds == 0:
                return _(b'now')
            if delta.seconds < 60:
                return ungettext(b'a second ago', b'%(count)s\xa0seconds ago', delta.seconds) % {b'count': delta.seconds}
            if delta.seconds // 60 < 60:
                count = delta.seconds // 60
                return ungettext(b'a minute ago', b'%(count)s\xa0minutes ago', count) % {b'count': count}
            count = delta.seconds // 60 // 60
            return ungettext(b'an hour ago', b'%(count)s\xa0hours ago', count) % {b'count': count}
        else:
            delta = value - now
            if delta.days != 0:
                return pgettext(b'naturaltime', b'%(delta)s from now') % {b'delta': defaultfilters.timeuntil(value, now)}
            if delta.seconds == 0:
                return _(b'now')
            if delta.seconds < 60:
                return ungettext(b'a second from now', b'%(count)s\xa0seconds from now', delta.seconds) % {b'count': delta.seconds}
            if delta.seconds // 60 < 60:
                count = delta.seconds // 60
                return ungettext(b'a minute from now', b'%(count)s\xa0minutes from now', count) % {b'count': count}
            count = delta.seconds // 60 // 60
            return ungettext(b'an hour from now', b'%(count)s\xa0hours from now', count) % {b'count': count}
        return