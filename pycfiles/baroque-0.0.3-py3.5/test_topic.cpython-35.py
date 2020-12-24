# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/entities/test_topic.py
# Compiled at: 2017-05-05 06:02:13
# Size of source mod 2**32: 1247 bytes
import pytest
from baroque.entities.topic import Topic
from baroque.defaults.eventtypes import GenericEventType, DataOperationEventType

def test_constructor_failures():
    with pytest.raises(TypeError):
        Topic()
        pytest.fail()
    with pytest.raises(AssertionError):
        Topic(123, [])
        pytest.fail()
    with pytest.raises(AssertionError):
        Topic('test', None)
        pytest.fail()
    with pytest.raises(AssertionError):
        Topic('test', 'abc')
        pytest.fail()
    with pytest.raises(AssertionError):
        Topic('test', ['abc'])
        pytest.fail()
    with pytest.raises(AssertionError):
        Topic('test', [], tags='abc')
        pytest.fail()


def test_constructor():
    t = Topic('test', [], description='this is a test topic', owner='me')
    assert t.id is not None
    assert len(t.eventtypes) == 0
    assert t.owner is not None
    assert len(t.tags) == 0
    assert t.timestamp is not None
    ets = [GenericEventType(), DataOperationEventType()]
    t = Topic('test', ets, description='this is a test topic', owner='me', tags=[
     'x', 'y'])
    assert len(t.eventtypes) == 2
    assert len(t.tags) == 2


def test_print():
    print(Topic('test', []))