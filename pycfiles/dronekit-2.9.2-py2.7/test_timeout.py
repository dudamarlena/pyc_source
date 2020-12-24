# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_timeout.py
# Compiled at: 2019-03-14 01:22:55
import time, socket
from dronekit import connect
from dronekit.test import with_sitl
from nose.tools import assert_equals

@with_sitl
def test_timeout(connpath):
    vehicle = connect(connpath, wait_ready=True, heartbeat_timeout=20)
    vehicle._handler._accept_input = False
    start = time.time()
    while vehicle._handler._alive and time.time() - start < 30:
        time.sleep(0.1)

    assert_equals(vehicle._handler._alive, False)
    vehicle.close()


def test_timeout_empty():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 5760))
    s.listen(1)
    try:
        vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True, heartbeat_timeout=20)
        vehicle.close()
        assert False
    except:
        pass