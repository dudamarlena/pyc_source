# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/dovetail/directives/test_packages.py
# Compiled at: 2012-08-01 03:51:57
"""py.test test script for packages.py"""
import packages, pytest
from pkg_resources import VersionConflict
SD = [
 'sooperdooper']
PL = ['pylint']
GOOD = ['pylint', 'coverage']
BAD = ['pylint', 'coverage', 'sooperdooper']
MANYB = ['silly1', 'silly2', 'silly3']
ERR = ['pylint>1000']

def setup_module(module):
    packages.install(GOOD)


class TestModules(object):

    def test_install(self):
        packages.install(PL)
        packages.install(GOOD)

    def test_cannot_install(self):
        with pytest.raises(packages.MissingRequirement):
            packages.install(BAD)

    def test_present(self):
        assert not packages.not_present(GOOD)

    def test_not_present(self):
        assert SD == packages.not_present(SD)

    def test_mixed(self):
        assert SD == packages.not_present(BAD)

    def test_multiple_not_present(self):
        assert MANYB == packages.not_present(MANYB, stop_on_error=False)
        assert ERR == packages.not_present(ERR, stop_on_error=False)

    def test_version_conflict(self):
        packages.install(PL)
        with pytest.raises(VersionConflict):
            packages.not_present(['pylint>1000'])

    def test_predicate(self):
        i = packages.Installed(*PL)
        print i
        assert i() is True
        i = packages.Installed(*GOOD)
        print i
        assert i() is True
        i = packages.Installed(*BAD)
        print i
        assert i() is False