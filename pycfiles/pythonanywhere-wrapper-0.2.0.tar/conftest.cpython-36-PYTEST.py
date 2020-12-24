# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trevor/projects/pythonanywhere-wrapper/source/tests/conftest.py
# Compiled at: 2017-10-21 10:41:04
# Size of source mod 2**32: 221 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from pythonanywhere_wrapper.client import PythonAnywhere

@pytest.fixture(scope='session')
def api_client():
    """Returns PythonAnywhere instance"""
    return PythonAnywhere('api_key', user='testuser')