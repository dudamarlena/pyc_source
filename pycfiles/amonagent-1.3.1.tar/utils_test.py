# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/martin/amonagent/tests/utils_test.py
# Compiled at: 2014-02-05 04:43:34
from amonagent.utils import *

class TestSystemUtils(object):

    def test_disk_volumes(self):
        volumes = get_disk_volumes()
        assert isinstance(volumes, list)
        for v in volumes:
            assert isinstance(v, str)

    def test_network_interfaces(self):
        interfaces = get_network_interfaces()
        assert isinstance(interfaces, list)
        for v in interfaces:
            assert isinstance(v, str)