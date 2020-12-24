# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/test/test_querythrottle.py
# Compiled at: 2009-05-01 11:44:33
"""
Tests for biblio.webquery.querythrottle, using nose.
"""
import time
from biblio.webquery import querythrottle

def test_waitonfail():
    throttle = querythrottle.WaitNSecondsThrottle(0.3)
    start_time = time.time()
    throttle.check_limit(None)
    new_time = time.time()
    assert new_time - start_time < 0.1
    throttle.check_limit(None)
    last_time = time.time()
    assert 0.3 < last_time - new_time
    return


def test_raiseonfail():
    throttle = querythrottle.WaitNSecondsThrottle(0.3, querythrottle.FAIL_AND_RAISE)
    start_time = time.time()
    throttle.check_limit(None)
    new_time = time.time()
    assert new_time - start_time < 0.1
    try:
        throttle.check_limit(None)
        assert "shouldn't get here"
    except:
        pass

    return


def test_waitnsecondsthrottle():
    throttle = querythrottle.WaitNSecondsThrottle(0.4)
    assert throttle.within_limit(None)
    throttle.log_success(None)
    assert not throttle.within_limit(None)
    time.sleep(0.2)
    assert not throttle.within_limit(None)
    time.sleep(0.3)
    assert throttle.within_limit(None)
    return


def test_waitonesecondthrottle():
    throttle = querythrottle.WaitOneSecondThrottle()
    assert throttle.within_limit(None)
    throttle.log_success(None)
    assert not throttle.within_limit(None)
    time.sleep(0.9)
    assert not throttle.within_limit(None)
    time.sleep(0.2)
    assert throttle.within_limit(None)
    return


def test_absolutenumberthrottle():
    throttle = querythrottle.AbsoluteNumberThrottle(5)
    for i in range(5):
        assert throttle.within_limit(None)
        throttle.log_success(None)

    assert not throttle.within_limit(None)
    throttle = querythrottle.AbsoluteNumberThrottle(5)
    for i in range(5):
        throttle.check_limit(None)

    try:
        throttle.check_limit(None)
        assert "shouldn't get here"
    except:
        pass

    return