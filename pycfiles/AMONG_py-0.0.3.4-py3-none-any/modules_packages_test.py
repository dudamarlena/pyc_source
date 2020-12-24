# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/martin/amonagent/tests/modules_packages_test.py
# Compiled at: 2014-05-20 04:17:01
from amonagent.modules.packages import system_packages

class TestGetPackagesForUpdate(object):

    def test_get_distro(self):
        result = system_packages.result()
        for value in result:
            assert 'current_version' in value.keys()
            assert 'new_version' in value.keys()
            assert 'name' in value.keys()