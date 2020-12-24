# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/datastructures/test_eventcounter.py
# Compiled at: 2017-03-23 14:00:43
# Size of source mod 2**32: 1450 bytes
import pytest
from baroque.datastructures.counters import EventCounter
from baroque.entities.event import Event
from baroque.defaults.eventtypes import GenericEventType, MetricEventType

def test_events_counting():
    eventtype1 = GenericEventType()
    eventtype2 = MetricEventType()
    c = EventCounter()
    assert c.count_all() == 0
    assert c.count(eventtype1) == 0
    assert c.count(eventtype2) == 0
    c.increment_counting(Event(eventtype1))
    assert c.count_all() == 1
    assert c.count(eventtype1) == 1
    assert c.count(eventtype2) == 0
    c.increment_counting(Event(eventtype2))
    assert c.count_all() == 2
    assert c.count(eventtype1) == 1
    assert c.count(eventtype2) == 1


def test_increment_counting():
    c = EventCounter()
    with pytest.raises(AssertionError):
        c.increment_counting('not-an-event')
        pytest.fail()


def test_dont_count_twice_eventtypes():
    eventtype = GenericEventType()
    same_eventtype = GenericEventType()
    c = EventCounter()
    assert c.count_all() == 0
    assert c.count(eventtype) == c.count(same_eventtype) == 0
    c.increment_counting(Event(eventtype))
    assert c.count_all() == 1
    assert c.count(eventtype) == 1
    assert c.count(same_eventtype) == 1
    c.increment_counting(Event(same_eventtype))
    assert c.count_all() == 2
    assert c.count(eventtype) == 2
    assert c.count(same_eventtype) == 2


def test_print():
    print(EventCounter())