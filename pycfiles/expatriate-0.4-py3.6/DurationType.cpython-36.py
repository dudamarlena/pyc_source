# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\DurationType.py
# Compiled at: 2018-01-18 12:29:16
# Size of source mod 2**32: 3813 bytes
import logging, re
from ..decorators import *
from .AnySimpleType import AnySimpleType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DurationType(AnySimpleType):

    def parse_value(self, value):
        m = re.fullmatch('-?P(\\d+Y)?(\\d+M)?(\\d+D)?(T(\\d+H)?(\\d+M)?(\\d+(\\.\\d+)?S)?)?', value)
        if not m or not re.fullmatch('.*[YMDHS].*', value) or not re.fullmatch('.*[^T]', value):
            raise ValueError('Unable to parse xs:Duration value')
        else:
            if value.startswith('-'):
                signed = True
            else:
                signed = False
            m = list(m.groups())
            m.insert(0, None)
            if m[1] is not None:
                years = int(m[1].strip('Y'))
            else:
                years = 0
            if m[2] is not None:
                months = int(m[2].strip('M'))
            else:
                months = 0
            if m[3] is not None:
                days = int(m[3].strip('D'))
            else:
                days = 0
            if m[5] is not None:
                hours = int(m[5].strip('H'))
            else:
                hours = 0
            if m[6] is not None:
                minutes = int(m[6].strip('M'))
            else:
                minutes = 0
            if m[7] is not None:
                seconds = float(m[7].strip('S'))
            else:
                seconds = 0.0
        months += years * 12
        hours += days * 24
        minutes += hours * 60
        seconds += minutes * 60.0
        if signed:
            return (-months, -seconds)
        else:
            return (
             months, seconds)

    def produce_value(self, value):
        if not isinstance(value, tuple):
            raise ValueError('xs:duration is produced from a months, seconds tuple')
        else:
            months, seconds = value
            if months < 0 or seconds < 0:
                r = '-P'
                months = -months
                seconds = -seconds
            else:
                r = 'P'
            years, months = divmod(months, 12)
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(int(minutes), 60)
            days, hours = divmod(hours, 24)
            if years != 0:
                r += '%dY' % years
            if months != 0:
                r += '%dM' % months
            if days != 0:
                r += '%dD' % days
            if hours != 0 or minutes != 0 or seconds != 0.0:
                r += 'T'
                if hours != 0:
                    r += '%dH' % hours
                if minutes != 0:
                    r += '%dM' % minutes
                if seconds != 0.0:
                    seconds_float = seconds - int(seconds)
                    if seconds_float != 0.0:
                        r += '%fS' % seconds
                    else:
                        r += '%dS' % int(seconds)
        return r