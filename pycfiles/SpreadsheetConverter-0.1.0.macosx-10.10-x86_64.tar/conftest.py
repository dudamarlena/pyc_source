# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/tests/conftest.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals
import os

def pytest_runtest_setup(item):
    base_dir = os.path.abspath(os.path.join(os.getcwd(), b'sample'))
    os.environ.setdefault(b'SSC_SEARCH_PATH', os.path.join(base_dir))
    os.environ.setdefault(b'SSC_YAML_SEARCH_PATH', os.path.join(base_dir, b'yaml'))
    os.environ.setdefault(b'SSC_YAML_SEARCH_RECURSIVE', b'1')
    os.environ.setdefault(b'SSC_XLS_SEARCH_PATH', os.path.join(base_dir, b'xls'))
    os.environ.setdefault(b'SSC_XLS_SEARCH_RECURSIVE', b'1')
    os.environ.setdefault(b'SSC_JSON_BASE_PATH', os.path.join(base_dir, b'json'))
    return b''