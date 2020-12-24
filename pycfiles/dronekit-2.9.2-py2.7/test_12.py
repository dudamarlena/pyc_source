# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_12.py
# Compiled at: 2019-03-14 01:22:55
import time
from dronekit import connect
from dronekit.test import with_sitl
from nose.tools import assert_equals

def current_milli_time():
    return int(round(time.time() * 1000))


@with_sitl
def test_timeout(connpath):
    v = connect(connpath, wait_ready=True)
    value = v.parameters['THR_MIN']
    assert_equals(type(value), float)
    start = current_milli_time()
    v.parameters['THR_MIN'] = value + 10
    end = current_milli_time()
    newvalue = v.parameters['THR_MIN']
    assert_equals(type(newvalue), float)
    assert_equals(newvalue, value + 10)
    assert end - start < 1000, 'time to set parameter was %s, over 1s' % (end - start,)
    v.close()