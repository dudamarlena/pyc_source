# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_mavlink.py
# Compiled at: 2019-03-14 01:22:55
import time
from dronekit import connect
from dronekit.mavlink import MAVConnection
from dronekit.test import with_sitl

@with_sitl
def test_mavlink(connpath):
    vehicle = connect(connpath, wait_ready=True)
    out = MAVConnection('udpin:localhost:15668')
    vehicle._handler.pipe(out)
    out.start()
    vehicle2 = connect('udpout:localhost:15668', wait_ready=True)
    result = {'success': False}

    @vehicle2.on_attribute('location')
    def callback(*args):
        result['success'] = True

    i = 20
    while not result['success'] and i > 0:
        time.sleep(1)
        i -= 1

    assert result['success']
    vehicle2.close()
    vehicle.close()