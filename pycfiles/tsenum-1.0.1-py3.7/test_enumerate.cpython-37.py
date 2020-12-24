# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tsenum/test_enumerate.py
# Compiled at: 2019-11-15 16:07:43
# Size of source mod 2**32: 2633 bytes
from . import enumerate_times
from datetime import datetime, timezone
from . import *
testdate = datetime(year=1970, month=1, day=10, hour=1, minute=20, second=33).astimezone(timezone.utc)

def test_formating():
    r = enumerate_times(testdate, 0, 1, STEP_DAY, '%Y')
    assert len(r) == 1
    assert '1970' in r
    r = enumerate_times(testdate, 0, 1, STEP_DAY, '%m')
    assert len(r) == 1
    assert '01' in r
    r = enumerate_times(testdate, 0, 1, STEP_DAY, '%d')
    assert len(r) == 1
    assert '10' in r


def test_3weeks():
    r = enumerate_times(testdate, 0, 3, STEP_WEEK, '%Y-%m-%d %H:%M:%S')
    assert len(r) == 3
    assert '1970-01-10 01:20:33' in r
    assert '1970-01-17 01:20:33' in r
    assert '1970-01-24 01:20:33' in r


def test_3days():
    r = enumerate_times(testdate, 0, 3, STEP_DAY, '%Y-%m-%d %H:%M:%S')
    assert len(r) == 3
    assert '1970-01-10 01:20:33' in r
    assert '1970-01-11 01:20:33' in r
    assert '1970-01-12 01:20:33' in r


def test_3minutes():
    r = enumerate_times(testdate, 0, 3, STEP_MINUTE, '%Y-%m-%d %H:%M:%S')
    assert len(r) == 3
    assert '1970-01-10 01:20:33' in r
    assert '1970-01-10 01:21:33' in r
    assert '1970-01-10 01:22:33' in r


def test_3seconds():
    r = enumerate_times(testdate, 0, 3, STEP_SECOND, '%Y-%m-%d %H:%M:%S')
    assert len(r) == 3
    assert '1970-01-10 01:20:33' in r
    assert '1970-01-10 01:20:34' in r
    assert '1970-01-10 01:20:35' in r


def test_invalid_stepsize():
    try:
        enumerate_times(testdate, 0, 3, 'invalid', '%Y-%m-%d %H:%M:%S')
        assert False
    except:
        assert True


def test_3seconds_minus_one():
    r = enumerate_times(testdate, -1, 3, STEP_SECOND, '%Y-%m-%d %H:%M:%S')
    assert len(r) == 3
    assert '1970-01-10 01:20:32' in r
    assert '1970-01-10 01:20:33' in r
    assert '1970-01-10 01:20:34' in r


def test_3seconds_minus_one():
    r = enumerate_times(testdate, 3, 3, STEP_SECOND, '%Y-%m-%d %H:%M:%S')
    assert len(r) == 3
    assert '1970-01-10 01:20:36' in r
    assert '1970-01-10 01:20:37' in r
    assert '1970-01-10 01:20:38' in r


def test_plus_3seconds():
    r = enumerate_times(testdate, 0, 3, STEP_SECOND, '%Y-%m-%d %H:%M:%S')
    assert len(r) == 3
    assert '1970-01-10 01:20:33' in r
    assert '1970-01-10 01:20:34' in r
    assert '1970-01-10 01:20:35' in r


def test_minus_3seconds():
    r = enumerate_times(testdate, 0, -3, STEP_SECOND, '%Y-%m-%d %H:%M:%S')
    assert len(r) == 3
    assert '1970-01-10 01:20:30' in r
    assert '1970-01-10 01:20:31' in r
    assert '1970-01-10 01:20:32' in r