# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/WebDAV/App_Common.py
# Compiled at: 2006-08-16 18:42:02
"""Commonly used utility functions."""
__version__ = '$Revision: 1.1 $'[11:-2]
import sys, os, time
from string import rfind
weekday_abbr = [
 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weekday_full = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
monthname = [
 None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def iso8601_date(ts=None):
    if ts is None:
        ts = time.time()
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(ts))


def rfc850_date(ts=None):
    if ts is None:
        ts = time.time()
    (year, month, day, hh, mm, ss, wd, y, z) = time.gmtime(ts)
    return '%s, %02d-%3s-%2s %02d:%02d:%02d GMT' % (weekday_full[wd], day, monthname[month], str(year)[2:], hh, mm, ss)


def rfc1123_date(ts=None):
    if ts is None:
        ts = time.time()
    (year, month, day, hh, mm, ss, wd, y, z) = time.gmtime(ts)
    return '%s, %02d %3s %4d %02d:%02d:%02d GMT' % (weekday_abbr[wd], day, monthname[month], year, hh, mm, ss)


def absattr(attr, c=callable):
    if c(attr):
        return attr()
    return attr


def aq_base(ob, hasattr=hasattr):
    if hasattr(ob, 'aq_base'):
        return ob.aq_base
    return ob


def is_acquired(ob, hasattr=hasattr, aq_base=aq_base, absattr=absattr):
    if not hasattr(ob, 'aq_parent'):
        return 0
    if hasattr(aq_base(ob.aq_parent), absattr(ob.id)):
        return 0
    if hasattr(aq_base(ob), 'isTopLevelPrincipiaApplicationObject') and ob.isTopLevelPrincipiaApplicationObject:
        return 0
    return 1


def package_home(globals_dict):
    __name__ = globals_dict['__name__']
    m = sys.modules[__name__]
    if hasattr(m, '__path__'):
        r = m.__path__[0]
    elif '.' in __name__:
        r = sys.modules[__name__[:rfind(__name__, '.')]].__path__[0]
    else:
        r = __name__
    return os.path.join(os.getcwd(), r)


def attrget(o, name, default):
    if hasattr(o, name):
        return getattr(o, name)
    return default


def Dictionary(**kw):
    return kw