# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testDateParsing.py
# Compiled at: 2010-03-22 23:48:32
"""
Unittests for dateutil.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testDateParsing.py 24358 2010-03-23 03:48:32Z dang $'
import calendar, math, random, time, unittest
from netlogger.tests import shared
from netlogger.nldate import completeISO, parseISO, guess
from netlogger.nldate import utcFormatISO, localtimeFormatISO
from netlogger.nldate import ISO8601, ENGLISH, SECONDS, UNKNOWN

class TestCase(shared.BaseTestCase):
    """Unit test cases.
    """
    NSAMP = 10000
    LOCALTIME = 99

    def testExhaustiveUTC(self):
        """Round-trip from numeric to string to numeric for UTC dates"""
        self._testExhaustive(utcFormatISO)

    def testExhaustiveLocaltime(self):
        """Round-trip from numeric to string to numeric for localtime"""
        self._testExhaustive(localtimeFormatISO)

    def _testExhaustive(self, format_fn):
        epsilon = 0.0001
        start = 0
        stop = 1237299999.99999
        num = 500
        step = (stop - start) / num
        sec = start
        while sec < stop:
            strdate = format_fn(sec)
            sec2 = parseISO(strdate)
            delta = sec2 - sec
            self.failUnless(-epsilon < delta < epsilon, 'round-trip failed. %.6lf -> %s -> %.6lf' % (
             sec, strdate, sec2))
            sec += step

    def testISO(self):
        """Convert ISO-like date strings to numeric dates
        """
        _r = random.randint
        for i in xrange(self.NSAMP):
            t = (
             _r(1970, 2037), _r(1, 12), _r(1, 28), _r(0, 11), _r(0, 59),
             _r(0, 59), _r(0, 999999))
            self._check(*t)

        self._check(1970, 1, 1, 0, 0, 0, 0)
        self._check(2037, 12, 31, 0, 0, 0, 0)
        for yr in xrange(1970, 2037, 3):
            for month in xrange(1, 12):
                if month == 2:
                    maxday = 28
                else:
                    maxday = 30
                day_skip = yr % 4 + 1
                for day in xrange(1, maxday, day_skip):
                    hr_skip = yr % 3 + 1
                    for hr in xrange(hr_skip):
                        sec = (yr + day + hr) % 60
                        min = yr * 365 % 60
                        self._check(yr, month, day, hr, min, sec, 0)

    def testGuess(self):
        """Guessing ability for date formats
        """

        def _pose(s, expected, expected_sec=-1):
            do_parse = expected_sec >= 0
            self.debug_('guess: %s' % s)
            (answer, sec) = guess(s, parse=do_parse)
            self.failUnless(answer == expected, "Date '%s' guessed as '%s', not expected '%s'" % (
             s, answer, expected))
            if do_parse:
                self.failUnless(sec == expected_sec, "Date '%s' type '%s' parsed to %lf not expected %lf" % (
                 s, answer, sec, expected_sec))

        _pose('', UNKNOWN)
        _pose('2000', ISO8601)
        _pose('yesterday', ENGLISH)
        _pose('1224028731', SECONDS)
        _pose('1224028731.1111222', SECONDS)
        _pose('-1.0', UNKNOWN)
        for i in xrange(1000):
            n = 123456789 + i + 0.123456 + i / 1000

        self.failUnless(guess('%lf' % n, set_gmt=True)[1] == n)
        _pose('2000Z', ISO8601, 946684800)
        now = time.time()
        for i in xrange(100):
            ltime = list(time.localtime(now))
            if ltime[2] == 1:
                ltime[2] = ltime[2] + 1
                english = 'tomorrow'
            else:
                ltime[2] = ltime[2] - 1
                english = 'yesterday'
            ltime[3] = ltime[4] = ltime[5] = 0
            partial = self._isostr(ltime, 0, self.LOCALTIME)
            iso_s = completeISO(partial)
            iso_sec = parseISO(iso_s)
            _pose(english, ENGLISH, iso_sec)
            time.sleep(0.01)

    def _check(self, year, mon, day, hour, min, sec, usec):
        self.debug_('Check year=%d month=%d day=%d hour=%d minute=%d second=%d usec=%d' % (
         year, mon, day, hour, min, sec, usec))
        tm_tuple = (
         year, mon, day, hour, min, sec, 0, 1, -1)
        is_dst = time.localtime(time.mktime(tm_tuple))[(-1)]
        tm_list = list(tm_tuple[:-1]) + [is_dst]
        prefix_len = random.choice((1, 3, len(tm_list)))
        tm_list_pfx = tm_list[:prefix_len]
        tm_list_full = [0, 1, 1, 0, 0, 0, -1, -1, -1]
        tm_list_full[:prefix_len] = tm_list[:prefix_len]
        if prefix_len < len(tm_list):
            usec = -1
        if prefix_len == 1:
            offset = random.choice((0, self.LOCALTIME))
        else:
            offset = random.choice((-7, 0, 3, self.LOCALTIME))
        s = self._isostr(tm_list_pfx, usec, offset)
        iso_s = completeISO(s)
        self.debug_("ISO date from '%s' => '%s'" % (s, iso_s))
        t2 = parseISO(iso_s)
        self.debug_("parse ISO date '%s' => %lf" % (iso_s, t2))
        if offset == self.LOCALTIME:
            self.debug_('localtime')
            expected = time.mktime(tm_list_full)
        else:
            self.debug_('random offset = %lf sec' % (offset * 3600))
            gm_tm = calendar.timegm(tm_list_full)
            expected = gm_tm - offset * 3600
        if usec >= 0:
            expected += usec / 1000000.0
        if abs(t2 - expected) - 3600 < 1e-05 and mon in (3, 4, 10, 11):
            return t2
        self.failUnless(abs(t2 - expected) < 1e-05, "parseISO of '%s'=>'%s' (year=%d month=%d day=%d hour=%d minute=%d second=%d usec=%d), result=%lf does not match expected=%lf (result - expected = %lf)" % (
         s, iso_s, year, mon, day, hour, min, sec, usec,
         t2, expected, t2 - expected))
        return t2

    def _isostr(self, values, usec, offset):
        """Build a prefix of an ISO8601 date.
        """
        fmt = ('%04d', '-%02d', '-%02d', 'T%02d', ':%02d', ':%02d')
        s = ('').join([ f % v for (f, v) in zip(fmt, values) ])
        if usec >= 0:
            s += '.%06d' % usec
        if offset == self.LOCALTIME:
            pass
        elif offset == 0:
            s += 'Z'
        else:
            if offset < 0:
                s += '-'
                abs_offset = -offset
            else:
                s += '+'
                abs_offset = offset
            s += '%02d:00' % abs_offset
        return s


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()