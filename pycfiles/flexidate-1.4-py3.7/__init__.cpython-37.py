# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flexidate/__init__.py
# Compiled at: 2019-03-26 11:30:29
# Size of source mod 2**32: 9776 bytes
import re, datetime
try:
    import dateutil.parser
    dateutil_parser = dateutil.parser.parser()
except:
    dateutil_parser = None

import sys

class FlexiDate(object):
    __doc__ = 'Store dates as strings and present them in a slightly extended version\n    of ISO8601.\n\n    Modifications:\n        * Allow a trailing qualifiers e.g. fl.\n        * Allow replacement of unknown values by ? e.g. if sometime in 1800s\n          can do 18??\n\n    Restriction on ISO8601:\n        * Truncation (e.g. of centuries) is *not* permitted.\n        * No week and day representation e.g. 1999-W01\n    '

    def __init__(self, year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None, qualifier=''):
        force = False
        self.year = self._cvt(year, rjust=4, force=force)
        self.month = self._cvt(month)
        self.day = self._cvt(day)
        self.hour = self._cvt(hour)
        self.minute = self._cvt(minute)
        self.second = self._cvt(second)
        self.microsecond = self._cvt(microsecond)
        self.qualifier = qualifier

    def _cvt(self, val, rjust=2, force=False):
        if val is not None:
            tmp = str(val).strip()
            if tmp.startswith('-'):
                tmp = '-' + tmp[1:].rjust(rjust, '0')
            else:
                tmp = tmp.rjust(rjust, '0')
            return tmp
        if force:
            return rjust * '!'
        return ''

    def __str__(self):
        out = self.isoformat()
        if self.qualifier:
            out += ' [%s]' % self.qualifier
        return out

    def __repr__(self):
        return '%s %s' % (self.__class__, self.__str__())

    def isoformat(self, strict=False):
        """Return date in isoformat (same as __str__ but without qualifier).

        WARNING: does not replace '?' in dates unless strict=True.
        """
        out = self.year
        for val in [self.month, self.day]:
            if not val:
                break
            out += '-' + val

        if strict:
            out = out.replace('?', '0')
        if self.hour:
            out += ' '
            out += self.hour
            for val in [self.minute, self.second]:
                if not val:
                    break
                out += ':' + val

            if self.microsecond:
                out += '.' + self.microsecond
        return out

    our_re_pat = '\n        (?P<year> -?[\\d?]+)\n        (?:\n                \\s* - (?P<month> [\\d?]{1,2})\n            (?: \\s* - (?P<day> [\\d?]{1,2}) )?\n            (?: \\s* - (?P<hour> [\\d?]{1,2}) )?\n            (?: \\s* - (?P<minute> [\\d?]{1,2}) )?\n            (?: \\s* - (?P<second> [\\d?]{1,2}) )?\n            (?: \\s* - (?P<microsecond> [\\d?]{1,2}) )?\n        )?\n        \\s*\n        (?: \\[ (?P<qualifier>[^]]*) \\])?\n        '
    our_re = re.compile(our_re_pat, re.VERBOSE)

    @classmethod
    def from_str(self, instr):
        """Undo affect of __str__"""
        if not instr:
            return FlexiDate()
        out = self.our_re.match(instr)
        if out is None:
            return
        return FlexiDate((out.group('year')),
          (out.group('month')),
          (out.group('day')),
          (out.group('hour')),
          (out.group('minute')),
          (out.group('second')),
          (out.group('microsecond')),
          qualifier=(out.group('qualifier')))

    def as_float(self):
        """Get as a float (year being the integer part).

        Replace '?' in year with 9 so as to be conservative (e.g. 19?? becomes
        1999) and elsewhere (month, day) with 0

        @return: float.
        """
        if not self.year:
            return
        out = float(self.year.replace('?', '9'))
        if self.month:
            out += float(self.month.replace('?', '0')) / 12.0
            if self.day:
                out += float(self.day.replace('?', '0')) / 365.0
        return out

    def as_datetime(self):
        """Get as python datetime.datetime.

        Require year to be a valid datetime year. Default month and day to 1 if
        do not exist.

        @return: datetime.datetime object.
        """
        year = int(self.year)
        month = int(self.month) if self.month else 1
        day = int(self.day) if self.day else 1
        hour = int(self.hour) if self.hour else 0
        minute = int(self.minute) if self.minute else 0
        second = int(self.second) if self.second else 0
        microsecond = int(self.microsecond) if self.microsecond else 0
        return datetime.datetime(year, month, day, hour, minute, second, microsecond)


def parse(date, dayfirst=True):
    """Parse a `date` into a `FlexiDate`.

    @param date: the date to parse - may be a string, datetime.date,
    datetime.datetime or FlexiDate.

    TODO: support for quarters e.g. Q4 1980 or 1954 Q3
    TODO: support latin stuff like M.DCC.LIII
    TODO: convert '-' to '?' when used that way
        e.g. had this date [181-]
    """
    if not date:
        return
    if isinstance(date, FlexiDate):
        return date
    if isinstance(date, int):
        return FlexiDate(year=date)
    if isinstance(date, datetime.datetime):
        parser = PythonDateTimeParser()
        return parser.parse(date)
    if isinstance(date, datetime.date):
        parser = PythonDateParser()
        return parser.parse(date)
    parser = DateutilDateParser()
    out = (parser.parse)(date, **{'dayfirst': dayfirst})
    if out is not None:
        return out
    val = 'UNPARSED: %s' % date
    val = val.encode('ascii', 'ignore')
    return FlexiDate(qualifier=val)


class DateParserBase(object):

    def parse(self, date):
        raise NotImplementedError

    def norm(self, date):
        return str(self.parse(date))


class PythonDateParser(object):

    def parse(self, date):
        return FlexiDate(date.year, date.month, date.day, 0, 0, 0, 0)


class PythonDateTimeParser(object):

    def parse(self, date):
        return FlexiDate(date.year, date.month, date.day, date.hour, date.minute, date.second, date.microsecond)


class DateutilDateParser(DateParserBase):
    _numeric = re.compile('^[0-9]+$')

    def parse(self, date, **kwargs):
        """
        :param **kwargs: any kwargs accepted by dateutil.parse function.
        """
        qualifiers = []
        if dateutil_parser is None:
            return
            date = orig_date = date.strip()
            date = date.replace('B.C.E.', 'BC')
            date = date.replace('BCE', 'BC')
            date = date.replace('B.C.', 'BC')
            date = date.replace('A.D.', 'AD')
            date = date.replace('C.E.', 'AD')
            date = date.replace('CE', 'AD')
            if date.startswith('-') or 'BC' in date or 'B.C.' in date:
                pre0AD = True
        else:
            pre0AD = False
        date = date.replace('BC', '')
        circa_match = re.match('([^a-zA-Z]*)c\\.?\\s*(\\d+.*)', date)
        if circa_match:
            qualifiers.append("Note 'circa'")
            date = ''.join(circa_match.groups())
        p_match = re.match('^p(\\d+)', date)
        if p_match:
            date = date[1:]
        uncertainty_match = re.match('([0-9xX]{4})\\?', date)
        if uncertainty_match:
            date = date[:-1]
            qualifiers.append('Uncertainty')
        res = (dateutil_parser._parse)(date, **kwargs)
        try:
            res = res[0]
        except:
            res = res

        if res is None:
            return
        if res.year is None and res.day:
            year = res.day
        else:
            if self._numeric.match(date):
                if len(date) == 2 or date.startswith('00'):
                    year = res.year % 100
                else:
                    year = res.year
            else:
                if pre0AD:
                    year = -year
                if not qualifiers:
                    qualifier = ''
                else:
                    qualifier = ', '.join(qualifiers) + ' : %s' % orig_date
            return FlexiDate(year, (res.month), (res.day), (res.hour), (res.minute), (res.second), (res.microsecond), qualifier=qualifier)