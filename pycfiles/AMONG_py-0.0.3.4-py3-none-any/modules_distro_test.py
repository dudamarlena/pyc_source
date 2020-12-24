# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/martin/amonagent/tests/modules_distro_test.py
# Compiled at: 2014-05-20 04:17:01
from amonagent.modules.distro import get_distro

class TestGetDistro(object):

    def test_get_distro(self):
        result = get_distro()
        assert isinstance(result, dict)
        assert 'release' in result
        assert 'id' in result
        assert 'type' in result