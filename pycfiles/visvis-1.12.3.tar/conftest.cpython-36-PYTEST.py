# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\dev\pylib\visvis\tests\conftest.py
# Compiled at: 2017-05-31 18:44:00
# Size of source mod 2**32: 202 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys, pytest

@pytest.fixture(scope='session', autouse=True)
def execute_before_any_test():
    if os.getenv('TEST_INSTALL') not in ('1', 'true'):
        sys.path.insert(0, '..')