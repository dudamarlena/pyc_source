# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/jeepney/jeepney/tests/test_bus.py
# Compiled at: 2020-01-10 16:25:36
# Size of source mod 2**32: 847 bytes
import pytest
from testpath import modified_env
from jeepney import bus

def test_get_connectable_addresses():
    a = list(bus.get_connectable_addresses('unix:path=/run/user/1000/bus'))
    if not a == ['/run/user/1000/bus']:
        raise AssertionError
    else:
        a = list(bus.get_connectable_addresses('unix:abstract=/tmp/foo'))
        assert a == ['\x00/tmp/foo']
    with pytest.raises(RuntimeError):
        list(bus.get_connectable_addresses('unix:tmpdir=/tmp'))


def test_get_bus():
    with modified_env({'DBUS_SESSION_BUS_ADDRESS':'unix:path=/run/user/1000/bus', 
     'DBUS_SYSTEM_BUS_ADDRESS':'unix:path=/var/run/dbus/system_bus_socket'}):
        if not bus.get_bus('SESSION') == '/run/user/1000/bus':
            raise AssertionError
        elif not bus.get_bus('SYSTEM') == '/var/run/dbus/system_bus_socket':
            raise AssertionError
    assert bus.get_bus('unix:path=/run/user/1002/bus') == '/run/user/1002/bus'