# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/datastructures/test_reactorsregistry.py
# Compiled at: 2017-03-28 19:08:36
# Size of source mod 2**32: 2628 bytes
import pytest
from baroque.datastructures.registries import ReactorsRegistry
from baroque.datastructures.bags import ReactorsBag
from baroque.entities.reactor import Reactor
from baroque.defaults.eventtypes import MetricEventType, GenericEventType, DataOperationEventType
from baroque.defaults.reactors import ReactorFactory

def test_get_or_create_bag_failing():
    reg = ReactorsRegistry()
    with pytest.raises(AssertionError):
        reg.get_or_create_bag('not-an-event-type')
        pytest.fail()


def test_get_or_create_bag_when_bag_doesnt_exist_yet():
    reg = ReactorsRegistry()
    et = MetricEventType
    assert et not in reg.registered_types
    result = reg.get_or_create_bag(et)
    assert et in reg.registered_types
    assert len(reg.registered_types) == 1
    assert isinstance(result, ReactorsBag)
    assert result == reg.registered_types[et]


def test_get_or_create_bag_when_bag_already_exists():
    reg = ReactorsRegistry()
    et1 = MetricEventType()
    et2 = GenericEventType()
    reg.get_or_create_bag(et1)
    assert len(reg.registered_types) == 1
    assert type(et1) in reg.registered_types
    assert type(et2) not in reg.registered_types
    result = reg.get_or_create_bag(et2)
    assert type(et2) in reg.registered_types
    assert len(reg.registered_types) == 2
    assert isinstance(result, ReactorsBag)
    assert result == reg.registered_types[type(et2)]


def test_get_bag():
    reg = ReactorsRegistry()
    et = MetricEventType()
    result = reg.get_bag(et)
    assert isinstance(result, ReactorsBag)
    reg.get_or_create_bag(et)
    result = reg.get_bag(MetricEventType)
    assert isinstance(result, ReactorsBag)
    assert result == reg.registered_types[type(et)]


def test_to():
    reg = ReactorsRegistry()
    et = MetricEventType()
    reg.get_or_create_bag(et)
    result = reg.to(et)
    assert result == reg.get_bag(et)


def test_to_any_event():
    reg = ReactorsRegistry()
    result = reg.to_any_event()
    assert result == reg.jolly_bag


def test_remove_all():
    reg = ReactorsRegistry()
    et1 = MetricEventType()
    et2 = GenericEventType()
    et3 = DataOperationEventType()
    reg.get_or_create_bag(et1)
    reg.get_or_create_bag(et2)
    reg.get_or_create_bag(et3)
    reg.get_jolly_bag().run(ReactorFactory.stdout())
    assert len(reg.registered_types) == 3
    assert len(reg.jolly_bag) == 1
    reg.remove_all()
    assert len(reg.registered_types) == 0
    assert len(reg.jolly_bag) == 0


def test_print():
    print(ReactorsRegistry())