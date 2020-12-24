# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trevor/projects/pythonanywhere/source/tests/conftest.py
# Compiled at: 2017-10-08 20:03:01
# Size of source mod 2**32: 213 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from pythonanywhere.client import PythonAnywhere

@pytest.fixture(scope='session')
def api_client():
    """Returns PythonAnywhere instance"""
    return PythonAnywhere('api_key', user='testuser')