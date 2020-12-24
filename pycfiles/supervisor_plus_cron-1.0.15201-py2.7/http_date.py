# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\medusa\http_date.py
# Compiled at: 2015-07-18 10:13:56
import re, time

def concat(*args):
    return ('').join(args)


def join(seq, field=' '):
    return field.join(seq)


def group(s):
    return '(' + s + ')'


short_days = [
 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
long_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
short_day_reg = group(join(short_days, '|'))
long_day_reg = group(join(long_days, '|'))
daymap = {}
for i in range(7):
    daymap[short_days[i]] = i
    daymap[long_days[i]] = i

hms_reg = join(3 * [group('[0-9][0-9]')], ':')
months = [
 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
monmap = {}
for i in range(12):
    monmap[months[i]] = i + 1

months_reg = group(join(months, '|'))
rfc822_date = join([
 concat(short_day_reg, ','),
 group('[0-9][0-9]?'),
 months_reg,
 group('[0-9]+'),
 hms_reg,
 'gmt'], ' ')
rfc822_reg = re.compile(rfc822_date)

def unpack_rfc822(m):
    g = m.group
    i = int
    return (
     i(g(4)),
     monmap[g(3)],
     i(g(2)),
     i(g(5)),
     i(g(6)),
     i(g(7)),
     0,
     0,
     0)


rfc850_date = join([
 concat(long_day_reg, ','),
 join([
  group('[0-9][0-9]?'),
  months_reg,
  group('[0-9]+')], '-'),
 hms_reg,
 'gmt'], ' ')
rfc850_reg = re.compile(rfc850_date)

def unpack_rfc850(m):
    g = m.group
    i = int
    return (
     i(g(4)),
     monmap[g(3)],
     i(g(2)),
     i(g(5)),
     i(g(6)),
     i(g(7)),
     0,
     0,
     0)


def build_http_date(when):
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(when))


def parse_http_date(d):
    d = d.lower()
    tz = time.timezone
    m = rfc850_reg.match(d)
    if m and m.end() == len(d):
        retval = int(time.mktime(unpack_rfc850(m)) - tz)
    else:
        m = rfc822_reg.match(d)
        if m and m.end() == len(d):
            retval = int(time.mktime(unpack_rfc822(m)) - tz)
        else:
            return 0
    if time.daylight and time.localtime(retval)[(-1)] == 1:
        retval += tz - time.altzone
    return retval