# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/vmalloc/pyrefactor/tests/conftest.py
# Compiled at: 2016-01-04 02:39:54
import pytest

@pytest.fixture(params=[
 '{b.c.d: 2}',
 '{@@@@@@}'])
def invalid_syntax(request):
    return request.param