# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_vehicleclass.py
# Compiled at: 2019-03-14 01:22:55
import time
from dronekit import connect, Vehicle
from dronekit.test import with_sitl

class DummyVehicle(Vehicle):

    def __init__(self, *args):
        super(DummyVehicle, self).__init__(*args)
        self.success = False

        def success_fn(self, name, m):
            self.success = True

        self.add_message_listener('HEARTBEAT', success_fn)


@with_sitl
def test_timeout(connpath):
    v = connect(connpath, vehicle_class=DummyVehicle)
    while not v.success:
        time.sleep(0.1)

    v.close()