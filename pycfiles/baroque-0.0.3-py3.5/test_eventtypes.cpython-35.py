# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/defaults/test_eventtypes.py
# Compiled at: 2017-03-23 14:00:10
# Size of source mod 2**32: 2075 bytes
from baroque.defaults import eventtypes
from baroque import Event, EventType

def test_generic_eventtype():
    et = eventtypes.GenericEventType()
    event = Event(et, payload=dict(test='value'))
    assert EventType.validate(event, et)
    print(et)


def test_state_transition_eventtype():
    et = eventtypes.StateTransitionEventType()
    event = Event(et)
    assert not EventType.validate(event, et)
    event = Event(et, payload={'from_status': 'A', 
     'to_status': 'B', 
     'trigger': 'system_failure', 
     'meta': {'key1': 'val1', 
              'key2': 'val2'}})
    assert EventType.validate(event, et)
    print(et)


def test_data_operation_eventtype():
    et = eventtypes.DataOperationEventType()
    event = Event(et)
    assert not EventType.validate(event, et)
    event = Event(et, payload={'datum': {'file': '/home/test.txt', 
               'char_position': 45}, 
     
     'operation': 'modify', 
     'timestamp': '2017-02-15T13:56:09Z', 
     'meta': {'old_char': 'F', 
              'new_char': 'N'}})
    assert EventType.validate(event, et)
    print(et)


def test_metric_eventtype():
    et = eventtypes.MetricEventType()
    event = Event(et)
    assert not EventType.validate(event, et)
    event = Event(et, payload={'metric': 'temperature', 
     'value': 56.7793, 
     'timestamp': '2017-02-15T13:56:09Z'})
    assert EventType.validate(event, et)
    print(et)