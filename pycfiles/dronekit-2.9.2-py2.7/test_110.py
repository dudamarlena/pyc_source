# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_110.py
# Compiled at: 2019-03-14 01:22:55
import time
from dronekit import connect, VehicleMode
from dronekit.test import with_sitl, wait_for
from nose.tools import assert_equals

@with_sitl
def test_110(connpath):
    vehicle = connect(connpath, wait_ready=True)
    vehicle.parameters['FS_GCS_ENABLE'] = 0
    vehicle.parameters['FS_EKF_THRESH'] = 100
    wait_for(lambda : vehicle.is_armable, 60)
    vehicle.mode = VehicleMode('GUIDED')
    time.sleep(3)

    def armed_callback(vehicle, attribute, value):
        armed_callback.called += 1

    armed_callback.called = 0
    vehicle.add_attribute_listener('armed', armed_callback)
    vehicle.add_attribute_listener('armed', armed_callback)
    vehicle.add_attribute_listener('armed', armed_callback)
    vehicle.add_attribute_listener('armed', armed_callback)
    vehicle.add_attribute_listener('armed', armed_callback)
    vehicle.armed = True
    time_max = 10
    wait_for(lambda : armed_callback.called, time_max)
    assert armed_callback.called > 0, 'Callback should have been called within %d seconds' % (time_max,)
    vehicle.remove_attribute_listener('armed', armed_callback)
    vehicle.remove_attribute_listener('armed', armed_callback)
    callcount = armed_callback.called
    vehicle.armed = False
    time.sleep(3)
    assert_equals(armed_callback.called, callcount, 'Callback should not have been called once removed.')
    vehicle.close()