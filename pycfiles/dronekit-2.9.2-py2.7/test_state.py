# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_state.py
# Compiled at: 2019-03-14 01:22:55
from dronekit import connect, SystemStatus
from dronekit.test import with_sitl
from nose.tools import assert_equals

@with_sitl
def test_state(connpath):
    vehicle = connect(connpath, wait_ready=['system_status'])
    assert_equals(type(vehicle.system_status), SystemStatus)
    assert_equals(type(vehicle.system_status.state), str)
    vehicle.close()