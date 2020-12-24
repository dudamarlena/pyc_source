# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blake/code/vivint-selenium-docker/tests/conftest.py
# Compiled at: 2017-11-06 17:12:00
# Size of source mod 2**32: 330 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from selenium_docker.base import ContainerFactory

@pytest.fixture(scope='module')
def factory():
    f = ContainerFactory.get_default_factory('unittests')
    f.scrub_containers()
    yield f
    f.stop_all_containers()