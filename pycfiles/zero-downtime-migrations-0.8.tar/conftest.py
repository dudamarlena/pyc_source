# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/smosker/zero-downtime-migrations/tests/conftest.py
# Compiled at: 2018-01-09 02:47:55
from __future__ import unicode_literals
import pytest
from test_app.models import TestModel

@pytest.fixture
def test_object():
    return TestModel.objects.create(name=b'some name')


@pytest.fixture
def test_object_two():
    return TestModel.objects.create(name=b'some other name')


@pytest.fixture
def test_object_three():
    return TestModel.objects.create(name=b'some different name')