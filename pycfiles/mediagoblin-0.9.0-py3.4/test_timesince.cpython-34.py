# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_timesince.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 2512 bytes
from datetime import datetime, timedelta
from mediagoblin.tools.timesince import timesince

def test_timesince():
    test_time = datetime.now()
    assert timesince(test_time, test_time + timedelta(microseconds=1)) == '0 minutes'
    assert timesince(test_time, test_time + timedelta(seconds=1)) == '0 minutes'
    assert timesince(test_time, test_time + timedelta(minutes=1)) == '1 minute'
    assert timesince(test_time, test_time + timedelta(minutes=2)) == '2 minutes'
    assert timesince(test_time, test_time + timedelta(hours=1)) == '1 hour'
    assert timesince(test_time, test_time + timedelta(hours=2)) == '2 hours'
    assert timesince(test_time, test_time + timedelta(days=1)) == '1 day'
    assert timesince(test_time, test_time + timedelta(days=2)) == '2 days'
    assert timesince(test_time, test_time + timedelta(days=7)) == '1 week'
    assert timesince(test_time, test_time + timedelta(days=14)) == '2 weeks'
    assert timesince(test_time, test_time + timedelta(days=30)) == '1 month'
    assert timesince(test_time, test_time + timedelta(days=60)) == '2 months'
    assert timesince(test_time, test_time + timedelta(days=365)) == '1 year'
    assert timesince(test_time, test_time + timedelta(days=730)) == '2 years'
    assert timesince(test_time, test_time + timedelta(days=5, hours=1)) == '5 days, 1 hour'
    assert timesince(test_time, test_time + timedelta(days=15)) == '2 weeks, 1 day'
    assert timesince(test_time, test_time + timedelta(days=97)) == '3 months, 1 week'
    assert timesince(test_time, test_time + timedelta(days=2250)) == '6 years, 2 months'