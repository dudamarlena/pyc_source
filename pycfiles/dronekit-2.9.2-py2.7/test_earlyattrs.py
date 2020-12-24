# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_earlyattrs.py
# Compiled at: 2019-03-14 01:22:55
from dronekit import connect
from dronekit.test import with_sitl
from nose.tools import assert_equals, assert_not_equals

@with_sitl
def test_battery_none(connpath):
    vehicle = connect(connpath, _initialize=False)
    assert_equals(vehicle.battery, None)
    vehicle.initialize()
    vehicle.wait_ready('battery')
    assert_not_equals(vehicle.battery, None)
    vehicle.close()
    return