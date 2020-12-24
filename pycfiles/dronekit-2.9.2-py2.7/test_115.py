# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_115.py
# Compiled at: 2019-03-14 01:22:55
import time
from dronekit import connect, VehicleMode
from dronekit.test import with_sitl
from nose.tools import assert_equals

@with_sitl
def test_115(connpath):
    v = connect(connpath, wait_ready=True)

    def mavlink_callback(*args):
        mavlink_callback.count += 1

    mavlink_callback.count = 0
    v.add_message_listener('*', mavlink_callback)
    v.mode = VehicleMode('STABILIZE')
    time.sleep(3)
    assert mavlink_callback.count > 0
    v.remove_message_listener('*', mavlink_callback)
    savecount = mavlink_callback.count
    v.armed = False
    time.sleep(3)
    assert_equals(savecount, mavlink_callback.count)
    v.armed = True
    time.sleep(3)
    v.close()