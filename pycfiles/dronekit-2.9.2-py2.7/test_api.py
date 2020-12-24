# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/unit/test_api.py
# Compiled at: 2019-03-14 01:22:55
from dronekit import VehicleMode
from nose.tools import assert_equals, assert_not_equals

def test_vehicle_mode_eq():
    assert_equals(VehicleMode('GUIDED'), VehicleMode('GUIDED'))


def test_vehicle_mode_neq():
    assert_not_equals(VehicleMode('AUTO'), VehicleMode('GUIDED'))