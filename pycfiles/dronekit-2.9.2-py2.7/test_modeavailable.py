# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_modeavailable.py
# Compiled at: 2019-03-14 01:22:55
"""
Simple test to trigger a bug in Vehicle class: issue #610 fixed in PR #611
"""
from dronekit import connect
from dronekit.test import with_sitl

@with_sitl
def test_timeout(connpath):
    v = connect(connpath)
    v._vehicle_type = 6
    v._autopilot_type = 8
    v._is_mode_available(0)
    v.close()