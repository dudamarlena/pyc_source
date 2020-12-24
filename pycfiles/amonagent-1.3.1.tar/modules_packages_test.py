# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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