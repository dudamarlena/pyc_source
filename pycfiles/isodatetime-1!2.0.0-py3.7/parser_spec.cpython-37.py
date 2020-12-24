# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/isodatetime/parser_spec.py
# Compiled at: 2019-01-30 07:03:09
# Size of source mod 2**32: 11490 bytes
"""This provides data to drive ISO 8601 parsing functionality."""
import re
from . import timezone
DATE_EXPRESSIONS = {'basic':{'complete':"\nCCYYMMDD\n+XCCYYMMDD  # '+' stands for either '+' or '-'\nCCYYDDD\n+XCCYYDDD\nCCYYWwwD\n+XCCYYWwwD", 
  'reduced':'\nCCYY-MM       # Deviation? Not clear if "basic" or "extended" in standard.\nCCYY\nCC\n+XCCYY-MM     # Deviation? Not clear if "basic" or "extended" in standard.\n+XCCYY\n+XCC\nCCYYWww\n+XCCYYWww', 
  'truncated':'\n-YYMM\n-YY\n--MMDD\n--MM\n---DD\nYYMMDD\nYYDDD\n-DDD\nYYWwwD\nYYWww\n-zWwwD\n-zWww\n-WwwD\n-Www\n-W-D\n'}, 
 'extended':{'complete':'\nCCYY-MM-DD\n+XCCYY-MM-DD\nCCYY-DDD\n+XCCYY-DDD\nCCYY-Www-D\n+XCCYY-Www-D', 
  'reduced':'\nCCYY-MM\n+XCCYY-MM\nCCYY-Www\n+XCCYY-Www', 
  'truncated':'\n-YY-MM\n--MM-DD\nYY-MM-DD\nYY-DDD\n-DDD          # Deviation from standard ?\nYY-Www-D\nYY-Www\n-z-WwwD\n-z-Www\n-Www-D\n'}}
TIME_EXPRESSIONS = {'basic':{'complete':'\n# No Time Zone\nhhmmss\n\n# No Time Zone - decimals\nhhmmss,tt\nhhmm,nn\nhh,ii\nhhmmss.tt\nhhmm.nn\nhh.ii\n', 
  'reduced':'\n# No Time Zone\nhhmm\nhh\n\n# No Time Zone - decimals\n', 
  'truncated':'\n# No Time Zone\n-mmss\n-mm\n--ss\n\n# No Time Zone - decimals\n-mmss,tt\n-mm,nn\n--ss,tt\n-mmss.tt\n-mm.nn\n--ss.tt\n'}, 
 'extended':{'complete':'\n# No Time Zone\nhh:mm:ss\n\n# No Time Zone - decimals\nhh:mm:ss,tt\nhh:mm,nn\nhh,ii          # Deviation? Not allowed in standard ?\nhh:mm:ss.tt\nhh:mm.nn\nhh.ii          # Deviation? Not allowed in standard ?\n', 
  'reduced':'\n# No Time Zone\nhh:mm\nhh             # Deviation? Not allowed in standard ?\n', 
  'truncated':'\n# No Time Zone\n-mm:ss\n-mm             # Deviation? Not allowed in standard ?\n--ss            # Deviation? Not allowed in standard ?\n\n# No Time Zone - decimals\n-mm:ss,tt\n-mm,nn          # Deviation? Not allowed in standard ?\n--ss,tt         # Deviation? Not allowed in standard ?\n-mm:ss.tt\n-mm.nn          # Deviation? Not allowed in standard ?\n--ss.tt         # Deviation? Not allowed in standard ?\n'}}
TIME_ZONE_EXPRESSIONS = {'basic':'\nZ\n+hh\n+hhmm\n', 
 'extended':'\nZ\n+hh             # Deviation? Not allowed in standard?\n+hh:mm\n'}
TIME_DESIGNATOR = 'T'
_DATE_TRANSLATE_INFO = [
 ('\\+(?=X)', '(?P<year_sign>[-+])', '%(year_sign)s', 'year_sign'),
 ('CC', '(?P<century>[0-9][0-9])', '%(century)02d', 'century'),
 ('YY', '(?P<year_of_century>[0-9][0-9])', '%(year_of_century)02d', 'year_of_century'),
 ('MM', '(?P<month_of_year>[0-9][0-9])', '%(month_of_year)02d', 'month_of_year'),
 ('DDD', '(?P<day_of_year>[0-9][0-9][0-9])', '%(day_of_year)03d', 'day_of_year'),
 ('DD', '(?P<day_of_month>[0-9][0-9])', '%(day_of_month)02d', 'day_of_month'),
 ('Www', 'W(?P<week_of_year>[0-9][0-9])', 'W%(week_of_year)02d', 'week_of_year'),
 ('D', '(?P<day_of_week>[0-9])', '%(day_of_week)01d', 'day_of_week'),
 ('z', '(?P<year_of_decade>[0-9])', '%(year_of_decade)01d', 'year_of_decade'),
 ('^---', '(?P<truncated>---)', '---', None),
 ('^--', '(?P<truncated>--)', '--', None),
 ('^-', '(?P<truncated>-)', '-', None)]
_TIME_TRANSLATE_INFO = [
 ('(?<=^hh)mm', '(?P<minute_of_hour>[0-9][0-9])', '%(minute_of_hour)02d', 'minute_of_hour'),
 ('(?<=^hh:)mm', '(?P<minute_of_hour>[0-9][0-9])', '%(minute_of_hour)02d', 'minute_of_hour'),
 ('(?<=^-)mm', '(?P<minute_of_hour>[0-9][0-9])', '%(minute_of_hour)02d', 'minute_of_hour'),
 ('^hh', '(?P<hour_of_day>[0-9][0-9])', '%(hour_of_day)02d', 'hour_of_day'),
 (',ii', ',(?P<hour_of_day_decimal>[0-9]+)', ',%(hour_of_day_decimal_string)s', 'hour_of_day_decimal_string'),
 ('\\.ii', '\\.(?P<hour_of_day_decimal>[0-9]+)', '.%(hour_of_day_decimal_string)s',
 'hour_of_day_decimal_string'),
 (',nn', ',(?P<minute_of_hour_decimal>[0-9]+)', ',%(minute_of_hour_decimal_string)s',
 'minute_of_hour_decimal_string'),
 ('\\.nn', '\\.(?P<minute_of_hour_decimal>[0-9]+)', '.%(minute_of_hour_decimal_string)s',
 'minute_of_hour_decimal_string'),
 ('ss', '(?P<second_of_minute>[0-9][0-9])', '%(second_of_minute)02d', 'second_of_minute'),
 (',tt', ',(?P<second_of_minute_decimal>[0-9]+)', ',%(second_of_minute_decimal_string)s',
 'second_of_minute_decimal_string'),
 ('\\.tt', '\\.(?P<second_of_minute_decimal>[0-9]+)', '.%(second_of_minute_decimal_string)s',
 'second_of_minute_decimal_string'),
 ('^--', '(?P<truncated>--)', '--', None),
 ('^-', '(?P<truncated>-)', '-', None)]
_TIME_ZONE_TRANSLATE_INFO = [
 ('mm', '(?P<time_zone_minute>[0-9][0-9])', '%(time_zone_minute_abs)02d', 'time_zone_minute_abs'),
 ('mm', '(?P<time_zone_minute>[0-9][0-9])', '%(time_zone_minute_abs)02d', 'time_zone_minute_abs'),
 ('hh', '(?P<time_zone_hour>[0-9][0-9])', '%(time_zone_hour_abs)02d', 'time_zone_hour_abs'),
 ('\\+', '(?P<time_zone_sign>[-+])', '%(time_zone_sign)s', 'time_zone_sign'),
 ('Z', '(?P<time_zone_utc>Z)', 'Z', None)]
LOCAL_TIME_ZONE_BASIC = timezone.get_local_time_zone_format()
LOCAL_TIME_ZONE_BASIC_NO_Z = LOCAL_TIME_ZONE_BASIC
if LOCAL_TIME_ZONE_BASIC_NO_Z == 'Z':
    LOCAL_TIME_ZONE_BASIC_NO_Z = '+0000'
LOCAL_TIME_ZONE_EXTENDED = timezone.get_local_time_zone_format(timezone.TimeZoneFormatMode.extended)
LOCAL_TIME_ZONE_EXTENDED_NO_Z = LOCAL_TIME_ZONE_EXTENDED
if LOCAL_TIME_ZONE_EXTENDED_NO_Z == 'Z':
    LOCAL_TIME_ZONE_EXTENDED_NO_Z = '+0000'
REC_SPLIT_STRFTIME_DIRECTIVE = re.compile('(%\\w)')
REC_STRFTIME_DIRECTIVE_TOKEN = re.compile('^%\\w$')
STRFTIME_TRANSLATE_INFO = {'%d':[
  'day_of_month'], 
 '%F':[
  'century', 'year_of_century', '-', 'month_of_year', '-',
  'day_of_month'], 
 '%H':[
  'hour_of_day'], 
 '%j':[
  'day_of_year'], 
 '%m':[
  'month_of_year'], 
 '%M':[
  'minute_of_hour'], 
 '%s':('(?P<seconds_since_unix_epoch>[0-9]+[,.]?[0-9]*)', '%(seconds_since_unix_epoch)s',
 'seconds_since_unix_epoch'), 
 '%S':[
  'second_of_minute'], 
 '%X':[
  'hour_of_day', ':', 'minute_of_hour', ':', 'second_of_minute'], 
 '%Y':[
  'century', 'year_of_century'], 
 '%z':[
  'time_zone_sign', 'time_zone_hour_abs', 'time_zone_minute_abs']}
STRPTIME_EXCLUSIVE_GROUP_INFO = {'%X':('%H', '%M', '%S'), 
 '%F':('%Y', '%y', '%m', '%d'), 
 '%s':tuple((i for i in STRFTIME_TRANSLATE_INFO if i != '%s'))}

class StrftimeSyntaxError(ValueError):
    __doc__ = 'An error denoting invalid or unsupported strftime/strptime syntax.'
    BAD_STRFTIME_INPUT = 'Invalid strftime/strptime representation: {0}'

    def __str__(self):
        return (self.BAD_STRFTIME_INPUT.format)(*self.args)


def get_date_translate_info(num_expanded_year_digits=2):
    """Return list of 4-element tuples with date translate information.

    returns:
        list: List tuples. Each tuple has 4 elements:
            - regex1 (str) - regex to match a date info substitution string
            - regex2 (str) - regex to capture date info
            - format (str) - template string to format date info
            - name (str) - name of this property
    """
    expanded_year_digit_regex = '[0-9]' * num_expanded_year_digits
    return _DATE_TRANSLATE_INFO + [
     (
      'X',
      '(?P<expanded_year>' + expanded_year_digit_regex + ')',
      '%(expanded_year_digits)0' + str(num_expanded_year_digits) + 'd',
      'expanded_year_digits')]


def get_time_translate_info():
    """Return list of 4-element tuples with time translate information.

    returns:
        list: List tuples. Each tuple has 4 elements:
            - regex1 (str) - regex to match a time info substitution string
            - regex2 (str) - regex to capture a time info
            - format (str) - template string to format time info
            - name (str) - name of this property
    """
    return _TIME_TRANSLATE_INFO


def get_time_zone_translate_info():
    """Return list of 4-element tuples with time zone translate information.

    returns:
        list: List tuples. Each tuple has 4 elements:
            - regex1 (str) - regex to match a time zone substitution string
            - regex2 (str) - regex to capture a time zone
            - format (str) - template string to format time zone
            - name (str) - name of this property
    """
    return _TIME_ZONE_TRANSLATE_INFO


def translate_strftime_token(strftime_token, num_expanded_year_digits=2):
    """Convert a strftime format into our own dump format."""
    return _translate_strftime_token(strftime_token,
      dump_mode=True, num_expanded_year_digits=num_expanded_year_digits)


def translate_strptime_token(strptime_token, num_expanded_year_digits=2):
    """Convert a strptime format into our own parsing format."""
    return _translate_strftime_token(strptime_token,
      dump_mode=False, num_expanded_year_digits=num_expanded_year_digits)


def _translate_strftime_token(strftime_token, dump_mode=False, num_expanded_year_digits=2):
    if strftime_token not in STRFTIME_TRANSLATE_INFO:
        raise StrftimeSyntaxError(strftime_token)
    else:
        our_translation = ''
        our_translate_info = get_date_translate_info(num_expanded_year_digits=num_expanded_year_digits) + get_time_translate_info() + get_time_zone_translate_info()
        attr_names = STRFTIME_TRANSLATE_INFO[strftime_token]
        if isinstance(attr_names, str):
            if dump_mode:
                return (
                 attr_names, [])
            return (
             re.escape(attr_names), [])
            if isinstance(attr_names, tuple):
                substitute, format_, name = attr_names
                if dump_mode:
                    our_translation += format_
        else:
            our_translation += substitute
        return (
         our_translation, [name])
    attr_names = list(attr_names)
    for attr_name in list(attr_names):
        for _, substitute, format_, name in our_translate_info:
            if name == attr_name:
                if dump_mode:
                    our_translation += format_
                else:
                    our_translation += substitute
                break
        else:
            our_translation += attr_name
            attr_names.remove(attr_name)

    return (
     our_translation, attr_names)