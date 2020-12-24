# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/postgresql_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
PostgreSQLConf - file ``/var/lib/pgsql/data/postgresql.conf``
=============================================================

The PostgreSQL configuration file is in a fairly standard 'key = value'
format, with the equals sign being optional.  A hash mark (#) marks the
rest of the line as a comment.

The configuration then appears as a dictionary in the `data` property.

This parser does not attempt to know the default value of any property; it
only shows what's defined in the configuration file as given.

This parser also provides several utility functions to make sense of values
specific to PostgreSQL.  These are:

  * `as_duration(property)`
      Convert the value (given in milliseconds, seconds, minutes, hours or
      days) to seconds (as a floating point value).
  * `as_boolean(property)`
      If the value is 'on', 'true', 'yes', or '1', return True.  If the value
      is 'off', 'false', 'no' or '0', return False.  Unique prefixes of these
      are acceptable and case is ignored.
  * `as_memory_bytes(property)`
      Convert a number given in KB, MB or GB into bytes, where 1 kilobyte is
      1024 bytes.

All three type conversion functions will raise a ValueError if the value
doesn't match the spec or cannot be converted to the correct type.

Example:
    >>> pgsql = shared[PostgreSQLConf]
    >>> 'port' in pgsql
    True
    >>> pgsql['port']
    '5432'
    >>>
"""
from .. import Parser, parser, get_active_lines, LegacyItemAccess
import re
from insights.specs import Specs

@parser(Specs.postgresql_conf)
class PostgreSQLConf(LegacyItemAccess, Parser):
    """
    Parses postgresql.conf and converts it into a dictionary of properties.
    """
    _value_error_str = "Do not recognise '{val}' for setting '{item}' " + 'as a {_type}'

    def parse_content(self, content):
        """
        Parsing rules from :

        https://www.postgresql.org/docs/9.3/static/config-setting.html

        One parameter is specified per line. The equal sign between name
        and value is optional. Whitespace is insignificant and blank lines
        are ignored.   Hash marks (#) designate the remainder of the line as
        a comment. Parameter values that are not simple identifiers or
        numbers must be single-quoted. To embed a single quote in a
        parameter value, write either two quotes (preferred) or
        backslash-quote.
        """
        pg_dict = {}
        for line in get_active_lines(content):
            if '=' in line:
                key, value = [ s.strip() for s in line.split('=', 1) ]
            else:
                key, value = [ s.strip() for s in line.split(' ', 1) ]
            if value[0] == "'" and value[(-1)] == "'":
                value = value[1:-1]
            if "''" in value:
                value = value.replace("''", "'")
            if "\\'" in value:
                value = value.replace("\\'", "'")
            pg_dict[key] = value

        self.data = pg_dict

    def as_duration(self, item, default=None):
        """
        Postgres's time durations for checkpoint_timeout can have 'ms', 's',
        'min', 'h', or 'd' suffixes.  We convert all of them here to seconds.

        See https://www.postgresql.org/docs/9.3/static/config-setting.html :-

        "Valid time units are ms (milliseconds), s (seconds), min (minutes),
        h (hours), and d (days)"

        We return a floating point number because of the possibility of
        convertion from milliseconds, and because maybe someone will say
        8.4h.
        """
        if not item:
            return
        else:
            if item in self.data:
                value = self.data[item]
            else:
                value = default
                if isinstance(value, int) or isinstance(value, float):
                    return float(value)
            dur_re = re.compile('^(?P<number>\\d+)(?P<suffix>ms|s|min|h|d)?$')
            length_of = {'ms': 0.001, 's': 1, 'min': 60, 'h': 3600, 'd': 86400}
            match = dur_re.search(value)
            if match:
                number, suffix = match.group('number', 'suffix')
                if suffix is None:
                    return float(number)
                return float(number) * length_of[suffix]
            raise ValueError(self._value_error_str.format(val=value, item=item, _type='duration'))
            return

    def as_boolean(self, item, default=None):
        """
        See https://www.postgresql.org/docs/9.3/static/config-setting.html :-

        "Boolean values can be written as on, off, true, false, yes, no, 1,
        0 (all case-insensitive) or any unambiguous prefix of these."
        """
        if not item:
            return
        else:
            if item in self.data:
                value = self.data[item]
            else:
                value = default
                if value is None or isinstance(value, bool):
                    return value
            lval = value.lower()
            if lval in ('on', 't', 'tr', 'tru', 'true', 'y', 'ye', 'yes', '1'):
                return True
            if lval in ('of', 'off', 'f', 'fa', 'fal', 'fals', 'false', 'n', 'no',
                        '0'):
                return False
            raise ValueError(self._value_error_str.format(val=value, item=item, _type='boolean'))
            return

    def as_memory_bytes(self, item, default=None):
        """
        See https://www.postgresql.org/docs/9.3/static/config-setting.html :-

        "Valid memory units are kB (kilobytes), MB (megabytes), and GB
        (gigabytes).  Note that the multiplier for memory units is 1024, not
        1000."
        """
        if not item:
            return
        else:
            size_of = {'kB': 1024, 'MB': 1048576, 'GB': 1073741824}
            if item in self.data:
                value = self.data[item]
            else:
                value = default
            if isinstance(value, int):
                return value
            if value.isdigit():
                return int(value)
            suffix = value[-2:]
            if suffix in size_of:
                return int(value[:-2]) * size_of[suffix]
            raise ValueError(self._value_error_str.format(val=value, item=item, _type='memory unit'))
            return