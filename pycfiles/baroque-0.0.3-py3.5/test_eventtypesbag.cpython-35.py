# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/datastructures/test_eventtypesbag.py
# Compiled at: 2017-03-23 14:00:59
# Size of source mod 2**32: 1079 bytes
import pytest
from baroque.datastructures.bags import EventTypesBag
from baroque.defaults.eventtypes import GenericEventType, MetricEventType, DataOperationEventType

def test_add():
    bag = EventTypesBag()
    assert len(bag.types) == 0
    ets = [GenericEventType(), MetricEventType()]
    bag.add(ets)
    assert len(bag.types) == 2
    bag.add([GenericEventType()])
    assert len(bag.types) == 2
    bag.add([DataOperationEventType()])
    assert len(bag.types) == 3


def test_add_failing():
    bag = EventTypesBag()
    with pytest.raises(AssertionError):
        bag.add('string')
        pytest.fail()
    with pytest.raises(AssertionError):
        bag.add(123)
        pytest.fail()
    with pytest.raises(AssertionError):
        ets = [
         GenericEventType(), dict()]
        bag.add(ets)
        pytest.fail()


def test_magic_methods():
    bag = EventTypesBag()
    assert len(bag) == 0
    et = GenericEventType()
    bag.add([et])
    assert len(bag) == 1
    assert et in bag
    for _ in bag:
        pass


def test_print():
    print(EventTypesBag())