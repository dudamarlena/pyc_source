# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/manuel/gcspypi/test/package_builder_test.py
# Compiled at: 2018-11-22 07:00:57
# Size of source mod 2**32: 1511 bytes
from ethronsoft.gcspypi.package.package_builder import PackageBuilder
from ethronsoft.gcspypi.exceptions import InvalidState
from pkg_resources import resource_filename
import os, sys, pytest

def test_src_tar():
    pkg_path = resource_filename(__name__, 'data/test_package-1.0.0.tar.gz')
    pkg = PackageBuilder(pkg_path).build()
    assert pkg.name == 'test-package'
    assert pkg.version == '1.0.0'
    assert pkg.requirements == set(['test-dep1', 'test-dep2'])
    assert pkg.type == 'SOURCE'


def test_src_wrong():
    pkg_path = resource_filename(__name__, 'data/WRONG-test_package-1.0.0.zip')
    with pytest.raises(InvalidState):
        PackageBuilder(pkg_path).build()


def test_wheel_wrong():
    pkg_path = resource_filename(__name__, 'data/WRONG-test_package-1.0.0-py2-none-any.whl')
    with pytest.raises(InvalidState):
        PackageBuilder(pkg_path).build()


def test_src_zip():
    pkg_path = resource_filename(__name__, 'data/test_package-1.0.0.zip')
    pkg = PackageBuilder(pkg_path).build()
    assert pkg.name == 'test-package'
    assert pkg.version == '1.0.0'
    assert pkg.requirements == set(['test-dep1', 'test-dep2'])
    assert pkg.type == 'SOURCE'


def test_wheel():
    pkg_path = resource_filename(__name__, 'data/test_package-1.0.0-py2-none-any.whl')
    pkg = PackageBuilder(pkg_path).build()
    assert pkg.name == 'test-package'
    assert pkg.version == '1.0.0'
    assert pkg.requirements == set(['test-dep1', 'test-dep2'])
    assert pkg.type == 'WHEEL'