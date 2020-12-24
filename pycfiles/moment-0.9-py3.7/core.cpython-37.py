# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/moment/core.py
# Compiled at: 2020-04-11 10:31:37
# Size of source mod 2**32: 3721 bytes
from calendar import timegm
from datetime import datetime, timedelta
from time import timezone
import pytz, times
from .date import MutableDate
from .parse import parse_date_and_formula, parse_js_date

class Moment(MutableDate):
    __doc__ = 'A class to abstract date difficulties.'

    def __init__(self, *args):
        date, formula = parse_date_and_formula(*args)
        self._date = date
        self._formula = formula

    @classmethod
    def now(cls):
        """Create a moment with the current datetime."""
        date = datetime.now()
        formula = '%Y-%m-%dT%H:%M:%S'
        return cls(date, formula)

    @classmethod
    def utc(cls, *args):
        """Create a moment from a UTC date."""
        date, formula = parse_date_and_formula(*args)
        date = pytz.timezone('UTC').localize(date)
        return cls(date, formula)

    @classmethod
    def utcnow(cls):
        """UTC equivalent to now."""
        date = pytz.timezone('UTC').localize(datetime.utcnow())
        formula = '%Y-%m-%dT%H:%M:%S'
        return cls(date, formula)

    @classmethod
    def unix(cls, timestamp, utc=False):
        """Create a date from a Unix timestamp."""
        if utc:
            func = datetime.utcfromtimestamp
        else:
            func = datetime.fromtimestamp
        try:
            date = func(timestamp)
        except ValueError:
            date = func(timestamp / 1000)

        if utc:
            date = date.replace(tzinfo=(pytz.utc))
        formula = '%Y-%m-%dT%H:%M:%S'
        return cls(date, formula)

    def locale(self, zone=None):
        """Explicitly set the time zone you want to work with."""
        if not zone:
            self._date = datetime.fromtimestamp(timegm(self._date.timetuple()))
        else:
            try:
                self._date = pytz.timezone(zone).normalize(self._date)
            except ValueError:
                self._date = self._date.replace(tzinfo=(pytz.timezone(zone)))

            return self

    def timezone(self, zone):
        """
        Change the time zone and affect the current moment's time. Note, a
        locality must already be set.
        """
        date = self._date
        try:
            try:
                date = times.to_local(times.to_universal(date), zone)
            except:
                date = times.to_local(date, zone)

        finally:
            self._date = date

        return self

    def format(self, formula):
        """Display the moment in a given format."""
        formula = parse_js_date(formula)
        return self._date.strftime(formula)

    def strftime(self, formula):
        """Takes a Pythonic format, rather than the JS version."""
        return self._date.strftime(formula)

    def diff(self, moment, measurement=None):
        """Return the difference between moments."""
        return self - moment

    def done(self):
        """Return the datetime representation."""
        return self._date

    def clone(self):
        """Return a clone of the current moment."""
        clone = Moment(self._date)
        clone._formula = self._formula
        return clone

    def copy(self):
        """Same as clone."""
        return self.clone()

    def __repr__(self):
        if self._date is not None:
            formatted = self._date.strftime('%Y-%m-%dT%H:%M:%S')
            return '<Moment(%s)>' % formatted
        return '<Moment>'

    def __str__(self):
        formatted = self._date.strftime('%Y-%m-%dT%H:%M:%S')
        tz = str.format('{0:+06.2f}', -float(timezone) / 3600)
        return formatted + tz