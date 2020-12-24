# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_goto.py
# Compiled at: 2016-10-17 18:12:11
"""
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)

The example demonstrates how to arm and takeoff in Copter and how to navigate to
points using Vehicle.simple_goto.

Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from dronekit.test import with_sitl
from nose.tools import assert_equals

@with_sitl
def test_goto(connpath):
    vehicle = connect(connpath, wait_ready=True)
    vehicle.parameters['FS_GCS_ENABLE'] = 0
    vehicle.parameters['FS_EKF_THRESH'] = 100

    def arm_and_takeoff(aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """
        i = 60
        while not vehicle.is_armable and i > 0:
            time.sleep(1)
            i = i - 1

        assert_equals(vehicle.is_armable, True)
        vehicle.mode = VehicleMode('GUIDED')
        i = 60
        while vehicle.mode.name != 'GUIDED' and i > 0:
            time.sleep(1)
            i = i - 1

        assert_equals(vehicle.mode.name, 'GUIDED')
        vehicle.armed = True
        i = 60
        while not vehicle.armed and vehicle.mode.name == 'GUIDED' and i > 0:
            time.sleep(1)
            i = i - 1

        assert_equals(vehicle.armed, True)
        vehicle.simple_takeoff(aTargetAltitude)
        while True:
            if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                break
            assert_equals(vehicle.mode.name, 'GUIDED')
            time.sleep(1)

    arm_and_takeoff(10)
    point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
    vehicle.simple_goto(point1)
    time.sleep(3)
    point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
    vehicle.simple_goto(point2)
    time.sleep(3)
    vehicle.mode = VehicleMode('RTL')
    vehicle.close()