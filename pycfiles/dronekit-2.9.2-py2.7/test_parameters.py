# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_parameters.py
# Compiled at: 2019-03-14 01:22:55
import time
from dronekit import connect
from dronekit.test import with_sitl
from nose.tools import assert_equals, assert_not_equals

@with_sitl
def test_parameters(connpath):
    vehicle = connect(connpath)
    assert_not_equals(vehicle.parameters.get('THR_MIN', wait_ready=True), None)
    try:
        assert_not_equals(vehicle.parameters['THR_MIN'], None)
    except:
        assert False

    assert_equals(vehicle.parameters.get('xXx_extreme_garbage_value_xXx', wait_ready=True), None)
    vehicle.close()
    return


@with_sitl
def test_iterating(connpath):
    vehicle = connect(connpath, wait_ready=True)
    for k, v in vehicle.parameters.items():
        break

    for key in vehicle.parameters:
        break

    vehicle.close()


@with_sitl
def test_setting(connpath):
    vehicle = connect(connpath, wait_ready=True)
    assert_not_equals(vehicle.parameters['THR_MIN'], None)
    result = {'success': False}

    @vehicle.parameters.on_attribute('THR_MIN')
    def listener(self, name, value):
        result['success'] = name == 'THR_MIN' and value == 3.0

    vehicle.parameters['THR_MIN'] = 3.0
    i = 5
    while not result['success'] and i > 0:
        time.sleep(1)
        i = i - 1

    assert_equals(result['success'], True)
    vehicle.close()
    return