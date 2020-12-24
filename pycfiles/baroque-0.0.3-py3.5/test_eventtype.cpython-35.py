# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/entities/test_eventtype.py
# Compiled at: 2017-03-23 13:58:42
# Size of source mod 2**32: 1659 bytes
import pytest
from baroque.entities.eventtype import EventType
from baroque.entities.event import Event
from baroque.defaults.eventtypes import GenericEventType

def test_constructor_failures():
    with pytest.raises(AssertionError):
        EventType(None)
        pytest.fail()
    with pytest.raises(AssertionError):
        EventType(123)
        pytest.fail()


def test_constructor():
    et = EventType('{}', description='hello', owner=1234)
    assert et.jsonschema == '{}'
    assert not et.tags
    assert et.owner == 1234
    assert et.description == 'hello'


def test_md5():
    et = EventType('{}', description='hello', owner=1234)
    assert et.md5() is not None


def test_validate():
    jsonschema = '{\n        "type": "object",\n        "properties": {\n            "payload": {\n                "type": "object",\n                "properties": {\n                    "foo": { "type": "string" },\n                    "bar": { "type": "number" }\n                },\n                "required": ["foo", "bar"]\n            }\n        },\n        "required": ["payload"]\n    }'
    eventtype = EventType(jsonschema)
    event = Event(eventtype, payload=dict(foo='value', bar=123))
    assert EventType.validate(event, eventtype)
    event = Event(GenericEventType(), payload=dict(foo='value', bar=123))
    assert not EventType.validate(event, eventtype)
    event = Event(eventtype, payload=dict(x=1, y=2))
    assert not EventType.validate(event, eventtype)


def test_print():
    print(EventType('{}'))