# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/vmalloc/pyrefactor/tests/conftest.py
# Compiled at: 2016-01-04 02:39:54
import pytest

@pytest.fixture(params=[
 '{b.c.d: 2}',
 '{@@@@@@}'])
def invalid_syntax(request):
    return request.param