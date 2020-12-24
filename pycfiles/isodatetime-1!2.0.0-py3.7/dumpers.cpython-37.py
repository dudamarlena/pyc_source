# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/isodatetime/dumpers.py
# Compiled at: 2019-01-30 07:03:09
# Size of source mod 2**32: 10219 bytes
"""This provides data model dumping functionality."""
import re
from . import parser_spec
from functools import lru_cache

class TimePointDumperBoundsError(ValueError):
    __doc__ = "An error raised when a TimePoint can't be dumped within bounds."
    MESSAGE = 'Cannot dump TimePoint {0}: {1} not in bounds {2} to {3}.'

    def __str__(self):
        return (self.MESSAGE.format)(*self.args)


class TimePointDumper(object):
    __doc__ = "Dump TimePoint instances to strings using particular formats.\n\n    A format can be specified in the self.dump method via the\n    formatting_string argument. Unlike Python's datetime strftime\n    method, this uses normal/Unicode character patterns to represent\n    which pieces of information to output where. A full reference\n    of valid patterns is found in the parser_spec module, with lots\n    of examples (coincidentally, used to generate the parsing).\n    Anything not matched will get left as it is in the string.\n    Specifying a particular time zone will result in a time zone\n    conversion of the date/time information before it is output.\n\n    For example, the following formatting_string\n    'CCYYMMDDThhmmZ' is made up of:\n    CC - year (century) information, e.g. 19\n    YY - year (decade, year of decade) information, e.g. 85\n    MM - month of year information, e.g. 05\n    DD - day of month information, e.g. 31\n    T - left alone, date/time separator\n    hh - hour of day information, e.g. 06\n    mm - minute of hour information, e.g. 58\n    Z - Zulu or UTC zero-offset time zone, left in, forces time zone\n    conversion\n    and might dump a TimePoint instance like this: '19850531T0658Z'.\n\n    Keyword arguments:\n    num_expanded_year_digits - an integer (default 2) that indicates\n    how many extra year digits to apply if appropriate (and if the\n    user requests that information).\n\n    "

    def __init__(self, num_expanded_year_digits=2):
        self._timepoint_parser = None
        self._rec_formats = {'date':[],  'time':[],  'time_zone':[]}
        self._time_designator = parser_spec.TIME_DESIGNATOR
        self.num_expanded_year_digits = num_expanded_year_digits
        for info, key in [
         (
          parser_spec.get_date_translate_info(num_expanded_year_digits),
          'date'),
         (
          parser_spec.get_time_translate_info(), 'time'),
         (
          parser_spec.get_time_zone_translate_info(), 'time_zone')]:
            for regex, _, format_sub, prop_name in info:
                rec = re.compile(regex)
                self._rec_formats[key].append((rec, format_sub, prop_name))

    def dump(self, timepoint, formatting_string):
        """Dump a timepoint according to formatting_string.

        The syntax for formatting_string is the syntax used for the
        TimePointParser internals. See TimePointParser.*_TRANSLATE_INFO.

        """
        if '%' in formatting_string:
            try:
                return self.strftime(timepoint, formatting_string)
            except TimePointDumperBoundsError:
                raise
            except ValueError:
                pass

        expression, properties, custom_time_zone = self._get_expression_and_properties(formatting_string)
        return self._dump_expression_with_properties(timepoint,
          expression, properties, custom_time_zone=custom_time_zone)

    def strftime(self, timepoint, formatting_string):
        """Implement equivalent of Python 2's datetime.datetime.strftime.

        Dump timepoint based on the format given in formatting_string.

        """
        split_format = parser_spec.REC_SPLIT_STRFTIME_DIRECTIVE.split(formatting_string)
        expression = ''
        properties = []
        for item in split_format:
            if parser_spec.REC_STRFTIME_DIRECTIVE_TOKEN.search(item):
                item_expression, item_properties = parser_spec.translate_strftime_token(item)
                expression += item_expression
                properties += item_properties
            else:
                expression += item

        return self._dump_expression_with_properties(timepoint, expression, properties)

    def _dump_expression_with_properties(self, timepoint, expression, properties, custom_time_zone=None):
        if not timepoint.truncated:
            if 'week_of_year' in properties or 'day_of_week' in properties:
                timepoint = 'month_of_year' in properties or 'day_of_month' in properties or 'day_of_year' in properties or timepoint.copy().to_week_date()
            else:
                if timepoint.get_is_week_date():
                    if 'month_of_year' in properties or 'day_of_month' in properties or 'day_of_year' in properties:
                        timepoint = timepoint.copy().to_calendar_date()
        elif custom_time_zone is not None:
            timepoint = timepoint.copy()
            if custom_time_zone == (0, 0):
                timepoint.set_time_zone_to_utc()
            else:
                current_time_zone = timepoint.get_time_zone()
                new_time_zone = current_time_zone.copy()
                new_time_zone.hours = custom_time_zone[0]
                new_time_zone.minutes = custom_time_zone[1]
                new_time_zone.unknown = False
                timepoint.set_time_zone(new_time_zone)
        property_map = {}
        for property_ in properties:
            property_map[property_] = timepoint.get(property_)
            if property_ == 'century':
                if not 'expanded_year_digits' not in properties:
                    min_value = self.num_expanded_year_digits or 0
                    max_value = 9999
                else:
                    if property_ == 'expanded_year_digits':
                        max_value = 10 ** (self.num_expanded_year_digits + 4) - 1
                        min_value = -max_value
                    else:
                        continue
                    value = timepoint.year
                if not min_value <= value <= max_value:
                    raise TimePointDumperBoundsError('year', value, min_value, max_value)

        return expression % property_map

    @lru_cache(maxsize=100000)
    def _get_expression_and_properties(self, formatting_string):
        date_time_strings = formatting_string.split(self._time_designator)
        date_string = date_time_strings[0]
        time_string = ''
        time_zone_string = ''
        custom_time_zone = None
        if len(date_time_strings) > 1:
            time_string = date_time_strings[1]
            if time_string.endswith('Z'):
                time_string = time_string[:-1]
                time_zone_string = 'Z'
                custom_time_zone = (0, 0)
            else:
                if '+hh' in time_string:
                    time_string, time_zone_string = time_string.split('+')
                    time_zone_string = '+' + time_zone_string
                else:
                    if '+' in time_string:
                        time_string, time_zone_string = time_string.split('+')
                        time_zone_string = '+' + time_zone_string
                        custom_time_zone = self.get_time_zone(time_zone_string)
                    else:
                        if '-' in time_string.lstrip('-'):
                            time_string, time_zone_string = time_string.split('-')
                            time_zone_string = '-' + time_zone_string
                            custom_time_zone = self.get_time_zone(time_zone_string)
        point_prop_list = []
        string_map = {'date':'', 
         'time':'',  'time_zone':''}
        for string, key in [(date_string, 'date'),
         (
          time_string, 'time'),
         (
          time_zone_string, 'time_zone')]:
            for rec, format_sub, prop in self._rec_formats[key]:
                new_string = rec.sub(format_sub, string)
                if new_string != string:
                    if prop is not None:
                        point_prop_list.append(prop)
                string = new_string

            string_map[key] = string

        expression = string_map['date']
        if string_map['time']:
            expression += self._time_designator + string_map['time']
        expression += string_map['time_zone']
        return (expression, tuple(point_prop_list), custom_time_zone)

    @lru_cache(maxsize=100000)
    def get_time_zone(self, time_zone_string):
        """Parse and return time zone from time_zone_string."""
        from . import parsers
        if self._timepoint_parser is None:
            self._timepoint_parser = parsers.TimePointParser()
        try:
            info = self._timepoint_parser.get_time_zone_info(time_zone_string)[1]
        except parsers.ISO8601SyntaxError:
            return
        else:
            info = self._timepoint_parser.process_time_zone_info(info)
            if info.get('time_zone_utc'):
                return (0, 0)
            if 'time_zone_hour' not in info:
                if 'time_zone_minute' not in info:
                    return
            hour = int(info.get('time_zone_hour', 0))
            minute = int(info.get('time_zone_minute', 0))
            return (hour, minute)