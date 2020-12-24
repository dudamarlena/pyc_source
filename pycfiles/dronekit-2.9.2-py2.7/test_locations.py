# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_locations.py
# Compiled at: 2019-03-14 01:22:55
import time
from dronekit import connect, VehicleMode
from dronekit.test import with_sitl, wait_for
from nose.tools import assert_equals, assert_not_equals

@with_sitl
def test_timeout(connpath):
    vehicle = connect(connpath, wait_ready=True)
    vehicle.parameters['FS_GCS_ENABLE'] = 0
    vehicle.parameters['FS_EKF_THRESH'] = 100

    def arm_and_takeoff(aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """
        wait_for(lambda : vehicle.is_armable, 60)
        assert_equals(vehicle.is_armable, True)
        vehicle.mode = VehicleMode('GUIDED')
        wait_for(lambda : vehicle.mode.name == 'GUIDED', 60)
        assert_equals(vehicle.mode.name, 'GUIDED')
        vehicle.armed = True
        wait_for(lambda : vehicle.armed, 60)
        assert_equals(vehicle.armed, True)
        vehicle.simple_takeoff(aTargetAltitude)
        while True:
            if vehicle.location.global_frame.alt >= aTargetAltitude * 0.95:
                break
            assert_equals(vehicle.mode.name, 'GUIDED')
            time.sleep(1)

    arm_and_takeoff(10)
    vehicle.wait_ready('location.local_frame', timeout=60)
    assert_not_equals(vehicle.location.local_frame.north, None)
    assert_not_equals(vehicle.location.local_frame.east, None)
    assert_not_equals(vehicle.location.local_frame.down, None)
    assert_not_equals(vehicle.location.global_frame.lat, None)
    assert_not_equals(vehicle.location.global_frame.lon, None)
    assert_not_equals(vehicle.location.global_frame.alt, None)
    assert_equals(type(vehicle.location.global_frame.lat), float)
    assert_equals(type(vehicle.location.global_frame.lon), float)
    assert_equals(type(vehicle.location.global_frame.alt), float)
    vehicle.close()
    return


@with_sitl
def test_location_notify(connpath):
    vehicle = connect(connpath)
    ret = {'success': False}

    @vehicle.location.on_attribute('global_frame')
    def callback(*args):
        assert_not_equals(args[2].alt, 0)
        ret['success'] = True

    wait_for(lambda : ret['success'], 30)
    assert ret['success'], 'Expected location object to emit notifications.'
    vehicle.close()