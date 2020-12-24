# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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