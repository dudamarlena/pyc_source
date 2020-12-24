# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_simpledemo.py
# Compiled at: 2019-03-14 01:22:55
"""
This test represents a simple demo for testing.
Feel free to copy and modify at your leisure.
"""
from dronekit import connect, VehicleMode
from dronekit.test import with_sitl
from nose.tools import assert_equals

@with_sitl
def test_parameter(connpath):
    v = connect(connpath, wait_ready=True)
    assert_equals(type(v.parameters['THR_MIN']), float)
    v.close()


@with_sitl
def test_mode(connpath):
    v = connect(connpath, wait_ready=True)
    assert isinstance(v.mode, VehicleMode)
    v.close()