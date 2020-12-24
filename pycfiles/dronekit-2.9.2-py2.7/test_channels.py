# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/test/sitl/test_channels.py
# Compiled at: 2019-03-14 01:22:55
import time
from dronekit import connect
from dronekit.test import with_sitl
from nose.tools import assert_equals

def assert_readback(vehicle, values):
    i = 10
    while i > 0:
        time.sleep(0.1)
        i -= 0.1
        for k, v in values.items():
            if vehicle.channels[k] != v:
                continue

        break

    if i <= 0:
        raise Exception('Did not match in channels readback %s' % values)


@with_sitl
def test_timeout(connpath):
    vehicle = connect(connpath, wait_ready=True)
    assert_equals(len(vehicle.channels), 8)
    assert_equals(len(vehicle.channels.overrides), 8)
    assert_equals(sorted(vehicle.channels.keys()), [ str(x) for x in range(1, 9) ])
    assert_equals(sorted(vehicle.channels.overrides.keys()), [])
    assert_equals(type(vehicle.channels['1']), int)
    assert_equals(type(vehicle.channels['2']), int)
    assert_equals(type(vehicle.channels['3']), int)
    assert_equals(type(vehicle.channels['4']), int)
    assert_equals(type(vehicle.channels['5']), int)
    assert_equals(type(vehicle.channels['6']), int)
    assert_equals(type(vehicle.channels['7']), int)
    assert_equals(type(vehicle.channels['8']), int)
    assert_equals(type(vehicle.channels[1]), int)
    assert_equals(type(vehicle.channels[2]), int)
    assert_equals(type(vehicle.channels[3]), int)
    assert_equals(type(vehicle.channels[4]), int)
    assert_equals(type(vehicle.channels[5]), int)
    assert_equals(type(vehicle.channels[6]), int)
    assert_equals(type(vehicle.channels[7]), int)
    assert_equals(type(vehicle.channels[8]), int)
    vehicle.channels.overrides = {'1': 1010}
    assert_readback(vehicle, {'1': 1010})
    vehicle.channels.overrides = {'2': 1020}
    assert_readback(vehicle, {'1': 1500, '2': 1010})
    vehicle.channels.overrides['1'] = 1010
    assert_readback(vehicle, {'1': 1010, '2': 1020})
    del vehicle.channels.overrides['1']
    assert_readback(vehicle, {'1': 1500, '2': 1020})
    vehicle.channels.overrides = {'1': 1010, '2': None}
    assert_readback(vehicle, {'1': 1010, '2': 1500})
    vehicle.channels.overrides['1'] = None
    assert_readback(vehicle, {'1': 1500, '2': 1500})
    try:
        vehicle.channels['9']
        assert False, 'Can read over end of channels'
    except:
        pass

    try:
        vehicle.channels['0']
        assert False, 'Can read over start of channels'
    except:
        pass

    try:
        vehicle.channels['1'] = 200
        assert False, 'can write a channel value'
    except:
        pass

    vehicle.channels.overrides = {'1': 1000}
    assert_readback(vehicle, {'1': 1000})
    vehicle.channels.overrides['2'] = 200
    assert_readback(vehicle, {'1': 200, '2': 200})
    vehicle.channels.overrides = {'2': 1010}
    assert_readback(vehicle, {'1': 1500, '2': 1010})
    vehicle.channels.overrides = {'3': 300, '4': 400, '5': 500, '6': 600, '7': 700}
    assert_readback(vehicle, {'3': 300, '4': 400, '5': 500, '6': 600, '7': 700})
    vehicle.channels.overrides = {'8': 800}
    assert_readback(vehicle, {'8': 800})
    vehicle.channels.overrides['8'] = 810
    assert_readback(vehicle, {'8': 810})
    try:
        vehicle.channels.overrides['9'] = 900
        assert False, 'can write channels.overrides 9'
    except:
        pass

    try:
        vehicle.channels.overrides = {'9': 900}
        assert False, 'can write channels.overrides 9 with braces'
    except:
        pass

    vehicle.channels.overrides['3'] = None
    assert '3' not in vehicle.channels.overrides, 'overrides hould not contain None'
    vehicle.channels.overrides = {'2': None}
    assert '2' not in vehicle.channels.overrides, 'overrides hould not contain None'
    vehicle.channels.overrides = {}
    assert_equals(len(vehicle.channels.overrides.keys()), 0)
    vehicle.channels.overrides = {'2': 33, '6': None}
    assert_readback(vehicle, {'2': 33, '6': 1500})
    assert_equals(list(vehicle.channels.overrides.keys()), ['2'])
    result = {'success': False}
    vehicle.channels.overrides = {}

    def channels_callback(vehicle, name, channels):
        if channels['3'] == 55:
            result['success'] = True

    vehicle.add_attribute_listener('channels', channels_callback)
    vehicle.channels.overrides = {'3': 55}
    i = 5
    while not result['success'] and i > 0:
        time.sleep(0.1)
        i -= 1

    assert result['success'], 'channels callback should be invoked.'
    vehicle.close()
    return