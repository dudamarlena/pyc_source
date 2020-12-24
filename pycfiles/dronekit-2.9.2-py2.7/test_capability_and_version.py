# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_capability_and_version.py
# Compiled at: 2019-03-14 01:22:55
import time
from dronekit import connect
from dronekit.test import with_sitl
from nose.tools import assert_false, assert_true

@with_sitl
def test_115(connpath):
    v = connect(connpath, wait_ready=True)
    time.sleep(5)
    assert_false(v.capabilities.ftp)
    start_time = time.time()
    slept = False
    while v.capabilities.mission_float == 0:
        if time.time() > start_time + 30:
            break
        time.sleep(0.1)
        slept = True

    if v.capabilities.mission_float:
        if slept:
            assert_true(v.version.major <= 3)
            assert_true(v.version_minor <= 3)
    else:
        assert_true(v.capabilities.mission_float)
    assert_true(v.version.major is not None)
    assert_true(len(v.version.release_type()) >= 2)
    assert_true(v.version.release_version() is not None)
    v.close()
    return